// Importa o React e outros módulos necessários
import { FC, useEffect, useState, useRef } from 'react';
import { useDraw } from '../hooks/useDraw';
import { ChromePicker } from 'react-color';

// Cria uma referência para o WebSocket
const socket = new WebSocket('ws://localhost:3001');

// Define o tipo Point
type Point = { x: number; y: number };

// Define o tipo Draw
type Draw = {
  prevPoint: Point | null;
  currentPoint: Point;
  ctx: CanvasRenderingContext2D | null;
};

// Define o tipo DrawLineProps
type DrawLineProps = {
  prevPoint: Point | null;
  currentPoint: Point;
  color: string;
};

// Define a página como um componente funcional
const Page: FC = () => {
  // Define o estado para a cor
  const [color, setColor] = useState<string>('#000');

  // Usa o hook useDraw para obter referências e funcionalidades relacionadas ao desenho
  const { canvasRef, onMouseDown, clear } = useDraw(createLine);

  // Usa o hook useRef para criar uma referência para o contexto do canvas
  const ctxRef = useRef<CanvasRenderingContext2D | null>(null);

  // Define o efeito colateral para lidar com a comunicação WebSocket
  useEffect(() => {
    // Obtém o contexto do canvas
    const ctx = canvasRef.current?.getContext('2d');
    ctxRef.current = ctx;

    // Adiciona os ouvintes de eventos do WebSocket
    socket.addEventListener('open', () => {
      console.log('WebSocket connection opened');
      socket.send(JSON.stringify({ type: 'client-ready' }));
    });

    socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);

      if (message.type === 'get-canvas-state') {
        if (!canvasRef.current?.toDataURL()) return;
        console.log('Sending canvas state');
        socket.send(JSON.stringify({ type: 'canvas-state', state: canvasRef.current.toDataURL() }));
      } else if (message.type === 'canvas-state-from-server') {
        console.log('Received canvas state');
        const img = new Image();
        img.src = message.state;
        img.onload = () => {
          ctx?.drawImage(img, 0, 0);
        };
      } else if (message.type === 'draw-line') {
        drawLine(message.data);
      } else if (message.type === 'clear') {
        clear();
      }
    });

    // Adiciona o ouvinte de eventos de fechamento do WebSocket
    socket.addEventListener('close', () => {
      console.log('WebSocket connection closed');
    });

    // Retorna uma função de limpeza para remover os ouvintes quando o componente é desmontado
    return () => {
      socket.close();
    };
  }, [canvasRef, clear]);

  // Função para criar uma linha no canvas e enviar a mensagem para o servidor
  function createLine({ prevPoint, currentPoint, ctx }: Draw) {
    const message = { type: 'draw-line', data: { prevPoint, currentPoint, color } };
    socket.send(JSON.stringify(message));
    drawLine({ prevPoint, currentPoint, ctx, color });
  }

  // Retorna a estrutura JSX da página
  return (
    <div className='w-screen h-screen bg-white flex justify-center items-center'>
      <div className='flex flex-col gap-10 pr-10'>
        <ChromePicker color={color} onChange={(e) => setColor(e.hex)} />
        <button type='button' className='p-2 rounded-md border border-black' onClick={() => socket.send(JSON.stringify({ type: 'clear' }))}>
          Clear canvas
        </button>
      </div>
      <canvas ref={canvasRef} onMouseDown={onMouseDown} width={750} height={750} className='border border-black rounded-md' />
    </div>
  );
};

// Exporta o componente como padrão
export default Page;
