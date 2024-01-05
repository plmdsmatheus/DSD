import express from 'express';
import http from 'http';
import WebSocket from 'ws';

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

type Point = { x: number; y: number };

type DrawLine = {
  prevPoint: Point | null;
  currentPoint: Point;
  color: string;
};

wss.on('connection', (ws: WebSocket) => {
  ws.on('message', (message: WebSocket.Data) => {
    const parsedMessage = JSON.parse(message.toString());

    if (parsedMessage.type === 'client-ready') {
      ws.send(JSON.stringify({ type: 'get-canvas-state' }));
    } else if (parsedMessage.type === 'canvas-state') {
      wss.clients.forEach((client: WebSocket) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: 'canvas-state-from-server', state: parsedMessage.state }));
        }
      });
    } else if (parsedMessage.type === 'draw-line') {
      wss.clients.forEach((client: WebSocket) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: 'draw-line', data: parsedMessage.data }));
        }
      });
    } else if (parsedMessage.type === 'clear') {
      wss.clients.forEach((client: WebSocket) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: 'clear' }));
        }
      });
    }
  });
});

server.listen(3001, () => {
  console.log('✔️ Server listening on port 3001');
});
