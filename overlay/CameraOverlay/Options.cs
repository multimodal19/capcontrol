using CommandLine;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CameraOverlay
{
    class Options
    {
        public Options() {
            Width = double.NaN;
            Height = double.NaN;
            FadeIn = 200;
            FadeOut = 200;
        }

        [Value(0, HelpText = "file path or URL pointing to image.")]
        public string ImageSource { get; set; }

        [Option('x', HelpText = "Horizontal offset (Default: 0).")]
        public double X { get; set; }

        [Option('y', HelpText = "Vertical offset (Default: 0).")]
        public double Y { get; set; }

        [Option('w', HelpText = "Width (Default: screen size).")]
        public double Width { get; set; }

        [Option('h', HelpText = "Width (Default: screen size).")]
        public double Height { get; set; }

        [Option('i', "fadein", HelpText = "Fade in duration in ms (Default: 200).")]
        public double FadeIn { get; set; }

        [Option('o', "fadeout", HelpText = "Fade out duration of previous image in ms (Default: 200).")]
        public double FadeOut { get; set; }

        [Option(HelpText = "Align image centered on the screen (Default: false).")]
        public bool Center { get; set; }

        [Option(HelpText = "Stretch image to fit (Default: only scale).")]
        public bool Stretch { get; set; }

        [Option(HelpText = "Animate gif (Default: false).")]
        public bool Animate { get; set; }
    }
}
