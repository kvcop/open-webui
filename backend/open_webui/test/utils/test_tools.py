
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from open_webui.utils.tools import get_tools
from open_webui.models.users import UserModel, UserSettings

@pytest.mark.asyncio
async def test_get_tools_injects_jira_header():
    # Mock dependencies
    mock_request = MagicMock()
    # Mock config state
    mock_request.app.state.config.TOOL_SERVER_CONNECTIONS = []

    # Mock User
    mock_user = MagicMock(spec=UserModel)
    mock_user.settings = UserSettings(ui={"jiraToken": "test-jira-token"})
    mock_user.id = "user1"

    # Mock Tools and other functions
    # Tools is imported in open_webui.utils.tools
    with patch("open_webui.utils.tools.Tools") as mock_tools_cls, \
         patch("open_webui.utils.tools.get_tool_servers", new_callable=AsyncMock) as mock_get_servers, \
         patch("open_webui.utils.tools.execute_tool_server", new_callable=AsyncMock) as mock_execute:

        mock_tools_cls.get_tool_by_id.return_value = None

        # Mock server data returned by get_tool_servers
        mock_get_servers.return_value = [{
            "id": "jira-server",
            "idx": 0,
            "specs": [{"name": "get_issue"}],
            "url": "http://jira",
            "info": {}
        }]

        # Mock config connections (accessed via request.app.state.config.TOOL_SERVER_CONNECTIONS)
        # The code uses tool_server_idx from tool_server_data (default 0)
        mock_request.app.state.config.TOOL_SERVER_CONNECTIONS = [{
            "auth_type": "none",
            "headers": {},
            "config": {}
        }]

        # Call get_tools with a tool_id that looks like "server:openapi:jira-server|get_issue"
        # Logic:
        # splits = tool_id.split(":")
        # len=3 -> type=splits[1] (openapi), server_id=splits[2] (jira-server|get_issue)
        # server_id_splits -> server_id="jira-server", function_names=["get_issue"]
        tool_ids = ["server:openapi:jira-server|get_issue"]

        tools = await get_tools(mock_request, tool_ids, mock_user, {})

        assert "get_issue" in tools
        callable_func = tools["get_issue"]["callable"]

        # Call the function to trigger execute_tool_server
        await callable_func()

        # Check arguments passed to execute_tool_server
        call_args = mock_execute.call_args
        assert call_args is not None
        _, kwargs = call_args

        headers = kwargs.get("headers", {})
        assert "Authorization-jira" in headers
        assert headers["Authorization-jira"] == "Token test-jira-token"

@pytest.mark.asyncio
async def test_get_tools_injects_confluence_header():
    # Mock dependencies
    mock_request = MagicMock()
    mock_request.app.state.config.TOOL_SERVER_CONNECTIONS = []

    mock_user = MagicMock(spec=UserModel)
    mock_user.settings = UserSettings(ui={"confluenceToken": "test-conf-token"})
    mock_user.id = "user1"

    with patch("open_webui.utils.tools.Tools") as mock_tools_cls, \
         patch("open_webui.utils.tools.get_tool_servers", new_callable=AsyncMock) as mock_get_servers, \
         patch("open_webui.utils.tools.execute_tool_server", new_callable=AsyncMock) as mock_execute:

        mock_tools_cls.get_tool_by_id.return_value = None

        mock_get_servers.return_value = [{
            "id": "confluence-server",
            "idx": 0,
            "specs": [{"name": "get_page"}],
            "url": "http://confluence",
            "info": {}
        }]

        mock_request.app.state.config.TOOL_SERVER_CONNECTIONS = [{
            "auth_type": "none",
            "headers": {},
            "config": {}
        }]

        tool_ids = ["server:openapi:confluence-server|get_page"]

        tools = await get_tools(mock_request, tool_ids, mock_user, {})

        assert "get_page" in tools
        callable_func = tools["get_page"]["callable"]

        await callable_func()

        call_args = mock_execute.call_args
        _, kwargs = call_args

        headers = kwargs.get("headers", {})
        assert "Authorization-confluence" in headers
        assert headers["Authorization-confluence"] == "Token test-conf-token"
