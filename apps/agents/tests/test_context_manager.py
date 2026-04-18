"""
Tests unitarios — `context_manager` y `db` (S5.3).

Todas las integraciones externas van mockeadas (Supabase, OpenAI/httpx, Anthropic).
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, Mock, patch
from uuid import UUID, uuid4

import pytest

from apps.agents.core import context_manager
from apps.agents.core.context_manager import (
    build_context,
    build_context_managed,
    compress_session,
    estimate_context_tokens,
)
from apps.agents.models.caso import ContextManagerInput, ContextoComprimido
from apps.agents.models.fase_output import FaseOutput
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.tools import db

from .conftest import fase_output_row_dict, hecho_row_dict


class TestBuildContext:
    """Casos obligatorios 1–3 y escenarios de error / borde."""

    @patch("apps.agents.core.context_manager._embed_query_text", return_value=[0.01] * 16)
    @patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[{"rol": "abogado", "contenido": "Hola"}])
    @patch(
        "apps.agents.core.context_manager.db.search_hechos_semanticos",
        return_value=[],
    )
    @patch("apps.agents.core.context_manager.db.get_outputs_fases", return_value=[])
    def test_build_context_total_tokens_est_positive(
        self,
        _mock_outputs: MagicMock,
        _mock_search: MagicMock,
        _mock_msgs: MagicMock,
        _mock_embed: MagicMock,
        caso_sayago_id: UUID,
        prompts_dir: Any,
    ) -> None:
        """1. `build_context` retorna `ContextoComprimido` con total_tokens_est > 0."""
        ctx = build_context(caso_sayago_id, "0E", prompts_dir=prompts_dir)
        assert isinstance(ctx, ContextoComprimido)
        assert ctx.total_tokens_est > 0
        assert ctx.total_tokens_est == estimate_context_tokens(ctx)

    @patch("apps.agents.core.context_manager._embed_query_text", return_value=[0.02] * 16)
    @patch(
        "apps.agents.core.context_manager.db.get_ultimos_mensajes",
        return_value=[{"rol": "abogado", "contenido": "x"}],
    )
    @patch(
        "apps.agents.core.context_manager.db.search_hechos_semanticos",
        return_value=[],
    )
    @patch("apps.agents.core.context_manager.db.get_outputs_fases", return_value=[])
    def test_build_context_under_default_token_cap(
        self,
        _mock_outputs: MagicMock,
        _mock_search: MagicMock,
        _mock_msgs: MagicMock,
        _mock_embed: MagicMock,
        caso_sayago_id: UUID,
        prompts_dir: Any,
    ) -> None:
        """2. Caso normal: no supera 25.000 tokens (límite por defecto)."""
        ctx = build_context(caso_sayago_id, "0E", prompts_dir=prompts_dir)
        assert ctx.total_tokens_est <= 25_000

    @patch("apps.agents.core.context_manager._embed_query_text", return_value=[0.03] * 16)
    @patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[])
    @patch("apps.agents.core.context_manager.db.get_outputs_fases", return_value=[])
    def test_build_context_caps_hechos_at_five_when_over_budget(
        self,
        _mock_outputs: MagicMock,
        _mock_msgs: MagicMock,
        _mock_embed: MagicMock,
        caso_sayago_id: UUID,
        prompts_dir: Any,
    ) -> None:
        """3. Si el contexto supera el límite, los hechos quedan como máximo en 5."""
        # Debe superar `max_tokens` con 10 hechos para disparar el recorte a 5, pero con 5 hechos
        # el encogedor (prompts, etc.) debe poder llevar el total bajo el techo.
        huge = "H" * 9_000
        diez = [
            Hecho(
                id=uuid4(),
                caso_id=caso_sayago_id,
                fase_origen="0E",
                contenido=huge,
                estatus_epistemico=EstatusEpistemico.verificado,
                fuente=None,
            )
            for _ in range(10)
        ]
        with patch(
            "apps.agents.core.context_manager.db.search_hechos_semanticos",
            return_value=diez,
        ):
            ctx = build_context(caso_sayago_id, "0E", max_tokens=1_000, prompts_dir=prompts_dir)
        assert len(ctx.hechos_relevantes) <= 5
        assert ctx.total_tokens_est <= 25_000

    @patch("apps.agents.core.context_manager.db.get_outputs_fases", return_value=[])
    @patch("apps.agents.core.context_manager.db.search_hechos_semanticos", return_value=[])
    @patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[])
    @patch("apps.agents.core.context_manager._embed_query_text", return_value=[0.04] * 8)
    def test_build_context_raises_if_fase_prompt_missing(
        self,
        _e: MagicMock,
        _s: MagicMock,
        _o: MagicMock,
        _g: MagicMock,
        caso_sayago_id: UUID,
        prompts_dir: Any,
    ) -> None:
        (prompts_dir / "fase_0e.md").unlink()
        with pytest.raises(FileNotFoundError):
            build_context(caso_sayago_id, "0E", prompts_dir=prompts_dir)

    def test_build_context_openai_key_missing_when_embedding_not_mocked(
        self,
        monkeypatch: pytest.MonkeyPatch,
        caso_sayago_id: UUID,
        prompts_dir: Any,
    ) -> None:
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with (
            patch("apps.agents.core.context_manager.db.get_outputs_fases", return_value=[]),
            patch("apps.agents.core.context_manager.db.search_hechos_semanticos", return_value=[]),
            patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[]),
        ):
            with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
                build_context(caso_sayago_id, "0E", prompts_dir=prompts_dir)

    @patch("apps.agents.core.context_manager._embed_query_text", return_value=[0.06] * 8)
    @patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[])
    @patch("apps.agents.core.context_manager.db.search_hechos_semanticos", return_value=[])
    @patch("apps.agents.core.context_manager.db.get_outputs_fases", return_value=[])
    def test_build_context_managed_respects_max_tokens(
        self,
        _go: MagicMock,
        _ss: MagicMock,
        _gu: MagicMock,
        _emb: MagicMock,
        caso_sayago_id: UUID,
        prompts_dir: Any,
    ) -> None:
        inp = ContextManagerInput(caso_id=caso_sayago_id, fase_actual="fase_0e", max_tokens=500)
        ctx = build_context_managed(inp, prompts_dir=prompts_dir)
        assert ctx.total_tokens_est <= 500

    def test_fase_prompt_filename_accepts_code_and_stem(self) -> None:
        """Borde: código de fase (`0E`) y stem (`fase_0e`) resuelven al mismo archivo."""
        assert context_manager._fase_prompt_filename("0E") == "fase_0e.md"
        assert context_manager._fase_prompt_filename("fase_0e") == "fase_0e.md"


class TestCompressSession:
    """Caso obligatorio 4 y errores."""

    @patch("apps.agents.core.context_manager.db.save_output_fase")
    @patch("apps.agents.core.context_manager.db.get_max_version_output_fase", return_value=0)
    @patch(
        "apps.agents.core.context_manager.db.get_mensajes_por_fase",
        return_value=[{"rol": "abogado", "contenido": "Mensaje de prueba"}],
    )
    @patch("anthropic.Anthropic")
    def test_compress_session_saves_with_aprobado_abogado_false(
        self,
        mock_anthropic_cls: MagicMock,
        _gm: MagicMock,
        _gv: MagicMock,
        mock_save: MagicMock,
        caso_sayago_id: UUID,
        anthropic_message_factory: Any,
    ) -> None:
        """4. `compress_session` persiste un `FaseOutput` con `aprobado_abogado = False`."""
        inst = MagicMock()
        mock_anthropic_cls.return_value = inst
        inst.messages.create.return_value = anthropic_message_factory("Resumen de sesión.", 50, 120)

        out = compress_session(caso_sayago_id, "0E", anthropic_model="claude-test-haiku")

        assert out.aprobado_abogado is False
        assert out.contenido.get("tipo") == "resumen_sesion"
        mock_save.assert_called_once()
        saved_arg: FaseOutput = mock_save.call_args[0][0]
        assert saved_arg.aprobado_abogado is False
        assert saved_arg.fase == "0E"

    @patch("apps.agents.core.context_manager.db.get_max_version_output_fase", return_value=3)
    @patch("apps.agents.core.context_manager.db.get_mensajes_por_fase", return_value=[{"a": 1}])
    @patch("anthropic.Anthropic")
    @patch("apps.agents.core.context_manager.db.save_output_fase")
    def test_compress_session_version_increments_from_db(
        self,
        _save: MagicMock,
        mock_anthropic_cls: MagicMock,
        _gm: MagicMock,
        _gv: MagicMock,
        caso_sayago_id: UUID,
        anthropic_message_factory: Any,
    ) -> None:
        inst = MagicMock()
        mock_anthropic_cls.return_value = inst
        inst.messages.create.return_value = anthropic_message_factory("v", 1, 2)
        out = compress_session(caso_sayago_id, "GEN", anthropic_model="m")
        assert out.version == 4

    @patch("apps.agents.core.context_manager.db.get_mensajes_por_fase", return_value=[])
    @patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[])
    @patch("apps.agents.core.context_manager.db.get_max_version_output_fase", return_value=0)
    @patch("anthropic.Anthropic")
    def test_compress_session_still_calls_model_with_empty_history(
        self,
        mock_anthropic_cls: MagicMock,
        _gv: MagicMock,
        _gu: MagicMock,
        _gm: MagicMock,
        caso_sayago_id: UUID,
        anthropic_message_factory: Any,
    ) -> None:
        """Borde: sin mensajes por fase ni fallback, igual se invoca al modelo."""
        inst = MagicMock()
        mock_anthropic_cls.return_value = inst
        inst.messages.create.return_value = anthropic_message_factory("", 0, 0)
        with patch("apps.agents.core.context_manager.db.save_output_fase"):
            compress_session(caso_sayago_id, "0A", anthropic_model="m")
        inst.messages.create.assert_called_once()

    @patch("apps.agents.core.context_manager.db.get_ultimos_mensajes", return_value=[])
    @patch(
        "apps.agents.core.context_manager.db.get_mensajes_por_fase",
        return_value=[{"rol": "abogado", "contenido": "x"}],
    )
    def test_compress_session_requires_anthropic_key(
        self,
        _gm: MagicMock,
        _gu: MagicMock,
        monkeypatch: pytest.MonkeyPatch,
        caso_sayago_id: UUID,
    ) -> None:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            compress_session(caso_sayago_id, "0E")


class TestDbGetOutputsFases:
    """Caso obligatorio 6."""

    def test_get_outputs_fases_only_queries_aprobado_true_and_returns_rows(
        self,
        patch_create_client: Any,
        caso_sayago_id: UUID,
    ) -> None:
        """6. Solo entradas aprobadas: la query filtra `aprobado_abogado = True` y el resultado es coherente."""
        row = fase_output_row_dict(
            caso_id=caso_sayago_id,
            fase="0E",
            version=1,
            contenido={"resumen": "Resumen corto de la fase 0E."},
            aprobado_abogado=True,
        )
        tb = MagicMock()
        sel = tb.select.return_value
        chain_end = sel.eq.return_value.eq.return_value.order.return_value.order.return_value
        chain_end.execute.return_value = Mock(data=[row])

        client = MagicMock()
        client.table.side_effect = lambda name: tb if name == "outputs_fases" else MagicMock()
        patch_create_client(client)

        results = db.get_outputs_fases(caso_sayago_id)
        assert len(results) == 1
        assert results[0].aprobado_abogado is True
        sel.eq.assert_called_once_with("caso_id", str(caso_sayago_id))
        sel.eq.return_value.eq.assert_called_once_with("aprobado_abogado", True)


class TestDbSearchHechosSemanticos:
    """Caso obligatorio 5."""

    def test_search_hechos_semanticos_fallback_when_rpc_fails(
        self,
        patch_create_client: Any,
        caso_sayago_id: UUID,
    ) -> None:
        """5. Si la RPC falla, se usa el fallback sobre la tabla `hechos`."""
        hid = uuid4()
        fallback_row = hecho_row_dict(hecho_id=hid, caso_id=caso_sayago_id, contenido="Hecho fallback")

        client = MagicMock()
        rpc_mid = MagicMock()
        rpc_mid.execute.side_effect = RuntimeError("RPC match_hechos no disponible")
        client.rpc.return_value = rpc_mid

        hechos_tb = MagicMock()
        hechos_chain = hechos_tb.select.return_value.eq.return_value.order.return_value.limit.return_value
        hechos_chain.execute.return_value = Mock(data=[fallback_row])

        def table_side_effect(name: str) -> MagicMock:
            if name == "hechos":
                return hechos_tb
            return MagicMock()

        client.table.side_effect = table_side_effect
        patch_create_client(client)

        out = db.search_hechos_semanticos(caso_sayago_id, [0.1, 0.2, 0.3], limit=10)
        assert len(out) == 1
        assert isinstance(out[0], Hecho)
        assert out[0].contenido == "Hecho fallback"
        client.rpc.assert_called_once()
        hechos_chain.execute.assert_called_once()


class TestDbOtherFunctions:
    """Cobertura adicional de `db.py` (sesiones, versión, guardado)."""

    def test_get_ultimos_mensajes_returns_chronological_order(
        self,
        patch_create_client: Any,
        caso_sayago_id: UUID,
    ) -> None:
        r1 = {"id": 1, "caso_id": str(caso_sayago_id), "contenido": "primero"}
        r2 = {"id": 2, "caso_id": str(caso_sayago_id), "contenido": "segundo"}
        tb = MagicMock()
        tb.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value = Mock(
            data=[r2, r1]
        )
        client = MagicMock()
        client.table.side_effect = lambda n: tb if n == "sesiones" else MagicMock()
        patch_create_client(client)

        msgs = db.get_ultimos_mensajes(caso_sayago_id, n=20)
        assert [m["contenido"] for m in msgs] == ["primero", "segundo"]

    def test_get_max_version_output_fase_zero_when_empty(
        self,
        patch_create_client: Any,
        caso_sayago_id: UUID,
    ) -> None:
        tb = MagicMock()
        inner = tb.select.return_value.eq.return_value.eq.return_value.order.return_value.limit.return_value
        inner.execute.return_value = Mock(data=[])
        client = MagicMock()
        client.table.side_effect = lambda n: tb if n == "outputs_fases" else MagicMock()
        patch_create_client(client)
        assert db.get_max_version_output_fase(caso_sayago_id, "0E") == 0

    def test_save_sesion_mensaje_includes_fase_when_provided(
        self,
        patch_create_client: Any,
        caso_sayago_id: UUID,
    ) -> None:
        tb = MagicMock()
        client = MagicMock()
        client.table.side_effect = lambda n: tb if n == "sesiones" else MagicMock()
        patch_create_client(client)
        db.save_sesion_mensaje(caso_sayago_id, "abogado", "Hola", fase="0E")
        tb.insert.assert_called_once()
        payload = tb.insert.call_args[0][0]
        assert payload["fase"] == "0E"

    def test_save_output_fase_payload_matches_model(
        self,
        patch_create_client: Any,
        caso_sayago_id: UUID,
    ) -> None:
        tb = MagicMock()
        client = MagicMock()
        client.table.side_effect = lambda n: tb if n == "outputs_fases" else MagicMock()
        patch_create_client(client)
        fo = FaseOutput(
            caso_id=caso_sayago_id,
            fase="0C",
            version=2,
            contenido={"k": "v"},
            aprobado_abogado=False,
            anotaciones="n",
            tokens_usados=10,
            costo_usd=0.001,
        )
        db.save_output_fase(fo)
        tb.insert.assert_called_once()
        p = tb.insert.call_args[0][0]
        assert p["aprobado_abogado"] is False
        assert p["fase"] == "0C"


class TestEstimateContextTokens:
    """Borde numérico del estimador."""

    def test_estimate_minimum_one_token_per_block(self) -> None:
        ctx = ContextoComprimido(
            prompt_maestro="",
            resumenes_fases=[],
            hechos_relevantes=[],
            ultimos_mensajes=[],
            prompt_fase="",
            total_tokens_est=0,
        )
        assert estimate_context_tokens(ctx) >= 5
