using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace CameraOverlay
{
    interface ICommandReader
    {
        event Action<string> OnCommandReceived;

        void Start();
        void Stop();
    }

    class TcpReader : ICommandReader
    {
        public event Action<string> OnCommandReceived;

        private bool running;
        private TcpListener server;
        private TcpClient client;

        public async void Start()
        {
            running = true;
            await Run();
        }

        public async Task Run()
        {
            try
            {
                // Only listen locally
                int port = 3000;
                IPAddress addr = IPAddress.Loopback;

                server = new TcpListener(addr, port);
                server.Start();
                Console.WriteLine($"Listening on {addr}:{port}");

                while (running)
                {
                    Console.WriteLine("Waiting for a connection...");
                    client = await server.AcceptTcpClientAsync();
                    Console.WriteLine("Connected!");


                    // Get stream to read and write
                    NetworkStream stream = client.GetStream();
                    string data = null;

                    using (StreamReader reader = new StreamReader(stream, Encoding.UTF8))
                    //using (StreamWriter writer = new StreamWriter(stream, Encoding.UTF8))
                    {
                        while ((data = await reader.ReadLineAsync()) != null)
                        {
                            if (!running) break;
                            OnCommandReceived.Invoke(data);

                            // Echo: send input back
                            //await writer.WriteAsync(data);
                            //await writer.FlushAsync();
                        }
                    }

                    client.Close();
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"TcpReader exception: {e}");
            }
            finally
            {
                server.Stop();
                Console.WriteLine("Stopped listening");
            }
        }

        public void Stop()
        {
            running = false;
            client?.Close();
            server?.Stop();
        }
    }

    class StdioReader : ICommandReader
    {
        public event Action<string> OnCommandReceived;
        private bool running;

        public async void Start()
        {
            running = true;
            await Run();
        }

        public async Task Run()
        {
            while (true)
            {
                // Read input asynchronously
                string input = await Task.Run(() => Console.ReadLine());

                // Check for end of Input stream
                if (input == null || !running) return;
                OnCommandReceived.Invoke(input);
            }
        }

        public void Stop()
        {
            running = false;
        }
    }


}
