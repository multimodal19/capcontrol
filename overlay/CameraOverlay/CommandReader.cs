using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using NetMQ;
using NetMQ.Sockets;

namespace CameraOverlay
{
    interface ICommandReader
    {
        event Action<string> OnCommandReceived;

        void Start();
        void Stop();
    }

    class ZMQReader : ICommandReader
    {
        public event Action<string> OnCommandReceived;

        private bool running;
        private readonly string topic;
        private readonly string addr;
        private SubscriberSocket socket;

        public ZMQReader(string topic, string addr)
        {
            this.topic = topic;
            this.addr = addr;
        }

        public void Start()
        {
            running = true;
            Run();
        }

        private async void Run()
        {
            try
            {
                // Create ZeroMQ Subscriber & subscribe to given topic
                socket = new SubscriberSocket();
                socket.Connect($"tcp://{addr}");
                socket.Subscribe(topic, Encoding.UTF8);
                Console.WriteLine($"Subscriber connected to {addr}");

                while (running)
                {
                    string msg = await Task.Run(() => {
                        try
                        {
                            return socket.ReceiveFrameString(Encoding.UTF8);
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine($"ZMQReader exception: {e}");
                            return null;
                        }
                    });
                    if (msg == null) continue;

                    // Only pass on the message, strip off topic!
                    OnCommandReceived.Invoke(msg.Substring(topic.Length + 1));
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"ZMQReader exception: {e}");
                socket.Close();
                Console.WriteLine("Stopped subscriber");
            }
        }

        public void Stop()
        {
            // Clean up
            running = false;
            socket?.Close();
        }
    }

    class StdioReader : ICommandReader
    {
        public event Action<string> OnCommandReceived;
        private bool running;

        public void Start()
        {
            running = true;
            Run();
        }

        public async void Run()
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
