using CommandLine;
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
using WpfAnimatedGif;

namespace CameraOverlay
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool rage = true;
        private Options rageImg = new Options() { ImageSource = "overlays/filter_rage.png", Center = true };
        private Options cloudImg = new Options() { ImageSource = "overlays/filter_clouds.png", Center = true };

        private List<ICommandReader> commandReaders = new List<ICommandReader>();

        public MainWindow()
        {
            InitializeComponent();

            // Get connection arguments if any - otherwise use default
            string addr = "localhost:4001";
            string[] args = Environment.GetCommandLineArgs();
            if (args.Length < 3)
            {
                Console.WriteLine($"No arguments specified, using default values!");
            }
            else
            {
                addr = $"{args[1]}:{args[2]}";
            }

            // Setup & start command readers
            commandReaders.Add(new StdioReader());
            commandReaders.Add(new ZMQReader("overlay", addr));
            commandReaders.ForEach(reader => reader.OnCommandReceived += HandleCommand);
            commandReaders.ForEach(reader => reader.Start());
        }

        private void HandleCommand(string command)
        {
            try
            {
                // Todo: Handle quoted arguments
                Parser.Default.ParseArguments<Options>(command.Trim().Split(' '))
                    .WithParsed(opts => ApplyOptions(opts));
            }
            catch(Exception) {}
        }

        private async void ApplyOptions(Options opts)
        {
            // First fade out old image if any
            await image.FadeOutAsync(TimeSpan.FromMilliseconds(opts.FadeOut));
            // Load new image & set attributes
            LoadImage(opts.ImageSource, opts.Animate);
            image.Height = opts.Height;
            image.Width = opts.Width;
            image.Margin = new Thickness(opts.X, opts.Y, 0, 0);
            image.Stretch = opts.Stretch ? Stretch.Fill : Stretch.Uniform;
            image.HorizontalAlignment = opts.Center ? HorizontalAlignment.Center : HorizontalAlignment.Left;
            image.VerticalAlignment = opts.Center ? VerticalAlignment.Center : VerticalAlignment.Top;
            // Finally fade in again
            await image.FadeInAsync(TimeSpan.FromMilliseconds(opts.FadeIn));
        }

        // Supports file paths & URLs
        private bool LoadImage(string imageSource, bool animate)
        {
            if (!Uri.TryCreate(imageSource, UriKind.RelativeOrAbsolute, out Uri imageUri))
            {
                Console.WriteLine($"Invalid image source: {imageSource}");
                return false;
            }

            Console.WriteLine($"Switching to new overlay: {imageSource}");
            if (animate)
            {
                ImageBehavior.SetAnimatedSource(image, new BitmapImage(imageUri));
            }
            else {
                ImageBehavior.SetAnimatedSource(image, null);
                image.Source = new BitmapImage(imageUri);
            }
            return true;
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
                    ApplyOptions(rage ? rageImg : cloudImg);
                    break;
            }
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            commandReaders.ForEach(reader => reader.Stop());
        }
    }
}
