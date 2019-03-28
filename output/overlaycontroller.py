import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 3000


class OverlayController:
    """Can send commands to the camera overlay."""

    def __init__(self):
        print(f"Connecting to {TCP_IP}:{TCP_PORT}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))

    def __del__(self):
        self.socket.close()

    def rage_overlay(self):
        """Show default rage overlay."""
        self.send_command("overlays/filter_rage.png", center=True)

    def cloud_overlay(self):
        """Show default cloud overlay."""
        self.send_command("overlays/filter_clouds.png", center=True)

    def send_command(self, overlay, x=None, y=None, width=None, height=None,
                     fade_in=None, fade_out=None, center=None, stretch=None, animate=None):
        """
        Send command to camera overlay.

        :param str overlay: new overlay source
        :param float x: horizontal offset
        :param float y: vertical offset
        :param float width: image width
        :param float height: image height
        :param float fade_in: fade in duration
        :param float fade_out: fade out duration
        :param bool center: center on screen
        :param bool stretch: stretch to fit bounds
        :param bool animate: animated gif
        """

        if overlay is None:
            raise TypeError("overlay source needs to be set!")

        # Build command but only use set arguments
        args = ""
        if x is not None:
            args += f" -x {x}"
        if y is not None:
            args += f" -y {y}"
        if width is not None:
            args += f" -w {width}"
        if height is not None:
            args += f" -h {height}"
        if fade_in is not None:
            args += f" -i {fade_in}"
        if fade_out is not None:
            args += f" -o {fade_out}"
        if center:
            args += " --center"
        if stretch:
            args += " --stretch"
        if animate:
            args += " --animate"

        command = f"{overlay}{args}\n"
        print(f"Overlay: {command}")
        self.socket.send(command.encode('utf8'))
