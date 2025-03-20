"""Main page."""

import streamlit as st
from extendable_agent.app.app_state import AppState
from extendable_agent.app.app_state import ensure_app_state
from extendable_agent.constants import PAGES
from extendable_agent.hub import ToolsHub


def load_function_names(app_state: AppState) -> list[str]:
    """Load function names from Tools Hub."""
    if not app_state.function_names:
        tools_hub = ToolsHub()
        app_state.function_names = tools_hub.get_file_list_from_github()
    return app_state.function_names


def function_selector(app_state: AppState) -> None:
    """Function selector."""
    # Get function names from Tools Hub
    function_names = load_function_names(app_state)
    selected_function_names = st.sidebar.multiselect(
        "Function or Pydantic model name",
        function_names,
    )
    app_state.selected_func_names = selected_function_names


@ensure_app_state
def main(app_state: AppState) -> None:
    """Main function."""
    pg = st.navigation(PAGES)

    function_selector(app_state)
    pg.run()
