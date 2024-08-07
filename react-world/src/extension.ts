

import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {


  const myViewProvider = new MyViewProvider(context.extensionUri);
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(MyViewProvider.viewType, myViewProvider)
    );

    let webview = vscode.commands.registerCommand('react-world.namasteworld', () => {

    let panel = vscode.window.createWebviewPanel("webview", "React", vscode.ViewColumn.One, {
            enableScripts: true
    })
    

    let scriptSrc = panel.webview.asWebviewUri(vscode.Uri.joinPath(context.extensionUri, "jbrowse-chat", "dist", "index.js"))

    let cssSrc = panel.webview.asWebviewUri(vscode.Uri.joinPath(context.extensionUri, "jbrowse-chat", "dist", "index.css"))

    panel.webview.html = `<!DOCTYPE html>
    <html lang="en">
      <head>
        <link rel="stylesheet" href="${cssSrc}" />
      </head>
      <body>
        <noscript>You need to enable JavaScript to run this app.</noscript>
        <div id="root"></div>
        <script src="${scriptSrc}"></script>
      </body>
    </html>
    `
});

    context.subscriptions.push(webview);
}

class MyViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'myCustomView';
  private readonly _extensionUri: vscode.Uri;

  constructor(extensionUri: vscode.Uri) {
    this._extensionUri = extensionUri;
  }

  resolveWebviewView(
    webviewView: vscode.WebviewView, 
    context: vscode.WebviewViewResolveContext, 
    token: vscode.CancellationToken
  ): Thenable<void> | void 
  {
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri]
      };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
 // Add logging to ensure messages are received
    webviewView.webview.onDidReceiveMessage(message => {
  console.log(`Received message: ${JSON.stringify(message)}`);
  switch (message.command) {
    case 'alert':
    vscode.window.showInformationMessage(message.text);
    return;
  }
  });
}

private _getHtmlForWebview(webview: vscode.Webview): string {
  return `<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Custom View</title>
  </head>
  <body>
    <h1>Hello from My Custom View!</h1>
    <button onclick="sendMessage()">Click me</button>
    <script>
    const vscode = acquireVsCodeApi();
    function sendMessage() {
      vscode.postMessage({ command: 'alert', text: 'Button clicked!' });
    }
    </script>
  </body>
  </html>`;
}

}
export function deactivate() { }