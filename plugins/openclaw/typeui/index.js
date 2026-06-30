import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "typebox";

const TYPEUI_MCP_URL = "https://mcp.typeui.sh";
const TYPEUI_MCP_SERVER = {
  url: TYPEUI_MCP_URL,
  transport: "streamable-http",
  auth: "oauth",
};

function isTypeUiMcpConfigured(server) {
  return (
    server?.url === TYPEUI_MCP_URL &&
    server?.transport === "streamable-http" &&
    server?.auth === "oauth"
  );
}

function getTypeUiMcpStatus(api) {
  const cfg = api.runtime.config.current();
  const server = cfg?.mcp?.servers?.typeui;

  return {
    configured: isTypeUiMcpConfigured(server),
    server,
  };
}

async function installTypeUiMcp(api, { force = false } = {}) {
  let wasConfigured = false;
  let changed = false;

  const result = await api.runtime.config.mutateConfigFile({
    afterWrite: { mode: "auto" },
    mutate(draft) {
      draft.mcp ??= {};
      draft.mcp.servers ??= {};

      const current = draft.mcp.servers.typeui;
      wasConfigured = isTypeUiMcpConfigured(current);

      if (wasConfigured && !force) {
        return;
      }

      draft.mcp.servers.typeui = {
        ...(typeof current === "object" && current ? current : {}),
        ...TYPEUI_MCP_SERVER,
      };
      changed = true;
    },
  });

  return {
    changed,
    wasConfigured,
    followUp: result?.followUp ?? result?.afterWrite,
  };
}

function formatInstallResult(result) {
  const firstLine = result.changed
    ? "TypeUI MCP has been installed in OpenClaw config."
    : "TypeUI MCP is already installed in OpenClaw config.";

  return [
    firstLine,
    "",
    "Next, authorize TypeUI OAuth:",
    "",
    "openclaw mcp login typeui",
    "",
    "Then verify the live MCP connection:",
    "",
    "openclaw mcp doctor typeui --probe",
  ].join("\n");
}

function formatStatusResult(status) {
  if (status.configured) {
    return [
      "TypeUI MCP is configured.",
      "",
      JSON.stringify(status.server, null, 2),
    ].join("\n");
  }

  return [
    "TypeUI MCP is not configured yet.",
    "",
    "Install it with:",
    "",
    "openclaw typeui install-mcp",
  ].join("\n");
}

export default definePluginEntry({
  id: "typeui",
  name: "TypeUI",
  description:
    "Connect OpenClaw-managed agents to TypeUI MCP for design skills, UI prompts, and layout variations.",
  register(api) {
    api.registerTool({
      name: "typeui_install_mcp",
      description: "Install the hosted TypeUI MCP server into OpenClaw config.",
      parameters: Type.Object({
        force: Type.Optional(Type.Boolean({
          description: "Overwrite the existing typeui MCP server entry if it is already present.",
        })),
      }),
      async execute(_id, params) {
        const result = await installTypeUiMcp(api, { force: Boolean(params?.force) });

        return {
          content: [{ type: "text", text: formatInstallResult(result) }],
        };
      },
    });

    api.registerTool({
      name: "typeui_mcp_status",
      description: "Show whether TypeUI MCP is installed in OpenClaw config.",
      parameters: Type.Object({}),
      async execute() {
        return {
          content: [{ type: "text", text: formatStatusResult(getTypeUiMcpStatus(api)) }],
        };
      },
    });

    api.registerCli(
      async ({ program }) => {
        const command = program
          .command("typeui")
          .description("Install and inspect TypeUI MCP for OpenClaw.");

        command
          .command("install-mcp")
          .description("Install the hosted TypeUI MCP server into OpenClaw config.")
          .option("--force", "Overwrite the existing typeui MCP server entry")
          .action(async (options) => {
            const result = await installTypeUiMcp(api, { force: Boolean(options.force) });
            console.log(formatInstallResult(result));
          });

        command
          .command("mcp-status")
          .description("Show whether TypeUI MCP is installed in OpenClaw config.")
          .action(() => {
            console.log(formatStatusResult(getTypeUiMcpStatus(api)));
          });
      },
      {
        descriptors: [
          {
            name: "typeui",
            description: "Install and inspect TypeUI MCP for OpenClaw.",
            hasSubcommands: true,
          },
        ],
      }
    );
  },
});
