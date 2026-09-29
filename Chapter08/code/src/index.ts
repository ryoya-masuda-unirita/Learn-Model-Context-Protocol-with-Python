import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// MCP サーバーを作る
const server = new McpServer({
  name: "demo-server",
  version: "1.0.0"
});

// 足し算の tool を追加する
server.registerTool("add",
  {
    title: "足し算 tool",
    description: "2つの数を足し算する",
    inputSchema: { a: z.number(), b: z.number() }
  },
  async ({ a, b }) => {
    return {
      content: [{ type: "text", text: String(a + b) }]
    };
  }
);

// stdin でメッセージを受け取り、stdout にメッセージを送り始める


async function main() {
    // stdio では stdout が MCP の通信に使われるので、メッセージは stderr に出す
    console.error("MCP サーバーを起動しています...");
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

main();
