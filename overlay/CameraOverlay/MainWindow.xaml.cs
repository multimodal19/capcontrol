using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace CameraOverlay
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool rage = true;
        private string rageImg = "overlays/filter_rage.png";
        private string cloudImg = "overlays/filter_clouds.png";

        private List<ICommandReader> commandReaders = new List<ICommandReader>();

        public MainWindow()
        {
            InitializeComponent();

            commandReaders.Add(new StdioReader());
            commandReaders.Add(new TcpReader());
            commandReaders.ForEach(reader => reader.OnCommandReceived += HandleCommand);
            commandReaders.ForEach(reader => reader.Start());
        }

        private void HandleCommand(string command)
        {
            LoadImage(command);
        }

        private void LoadImage(string imagePath)
        {
            if (!System.IO.File.Exists(imagePath))
            {
                Console.WriteLine($"File not found: {imagePath}");
                return;
            }

            Console.WriteLine($"Switching to new overlay: {imagePath}");
            image.TransitionSource(new BitmapImage(new Uri(imagePath, UriKind.RelativeOrAbsolute)));
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.Key)
            {
                // Close application on escape
                case Key.Escape:
                    Application.Current.Shutdown();
                    break;
                // Toggle between images on space
                case Key.Space:
                    rage = !rage;
                    LoadImage(rage ? rageImg : cloudImg);
                    break;
            }
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            commandReaders.ForEach(reader => reader.Stop());
        }
    }
}
