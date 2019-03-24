using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;

namespace CameraOverlay
{
    static class Extensions
    {
        public static Task FadeOutAsync(this Image image, TimeSpan fadeOutTime)
        {
            return FadeAsync(image, fadeOutTime, 0);
        }

        public static Task FadeInAsync(this Image image, TimeSpan fadeInTime)
        {
            return FadeAsync(image, fadeInTime, 1);
        }

        // Awaitable fade animation extension
        public static Task FadeAsync(this Image image, TimeSpan fadeTime, double targetOpacity)
        {
            var tcs = new TaskCompletionSource<bool>();

            if (image.Source != null && fadeTime != TimeSpan.Zero)
            {
                var fadeInAnimation = new DoubleAnimation(targetOpacity, fadeTime);
                fadeInAnimation.Completed += (o, e) => tcs.SetResult(true);
                image.BeginAnimation(Image.OpacityProperty, fadeInAnimation);
                return tcs.Task;
            }
            else
            {
                image.Opacity = targetOpacity;
                tcs.SetResult(true);
                return tcs.Task;
            }
        }
    }
}
