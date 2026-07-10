import pygame as pg
from pc_constants import SCREEN_WIDTH


def wrap_text(text: str, font: pg.Font, max_width: int) -> list[str]:
    """Wrap text into multiple lines constrained by pixel width.

    Preserves paragraph breaks from newline separators and wraps words
    without splitting them.

    Args:
        text (str): Input text to wrap.
        font (pg.Font): Font used to measure rendered width.
        max_width (int): Maximum width per line in pixels.

    Returns:
        list[str]: Wrapped lines ready for rendering.
    """

    lines: list[str] = []
    paragraphs = text.strip().split("\n")

    for paragraph in paragraphs:
        if paragraph.strip() == "":
            lines.append("")
            continue

        words = paragraph.split(" ")
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

    return lines


class PCUIElement:
    """Base UI element with text rendering and framed box styling."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pg.Font,
        text: str = "",
        bg_color: str = "black",
        text_color: str = "yellow",
        border_color: str = "yellow",
        border_radius: int = 12,
        max_lines: int = 2
    ) -> None:
        """Initialize UI element geometry, style, and text content.

        Args:
            x (int): Left position in pixels.
            y (int): Top position in pixels.
            width (int): Element width in pixels.
            height (int): Element height in pixels.
            font (pg.Font): Font used to render text.
            text (str, optional): Element text content.
            bg_color (str, optional): Background color.
            text_color (str, optional): Text color.
            border_color (str, optional): Border color.
            border_radius (int, optional): Rounded corner radius.
            max_lines (int, optional): Maximum rendered text lines.
        """

        self.rect = pg.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.max_lines = max_lines

    def wrap_text(self, max_width: int) -> list[str]:
        """Wrap and clamp element text to fit the given width.

        Applies paragraph-aware wrapping and truncates overflow lines with
        ellipsis when exceeding ``max_lines``.

        Args:
            max_width (int): Maximum width per line in pixels.

        Returns:
            list[str]: Wrapped (and possibly truncated) lines.
        """

        lines: list[str] = []
        paragraphs = self.text.strip().split("\n")

        for paragraph in paragraphs:
            if paragraph.strip() == "":
                lines.append("")
                continue
            words = paragraph.split(" ")
            current_line = words[0]
            for word in words[1:]:
                test_line = current_line + " " + word
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)

        if len(lines) > self.max_lines:
            lines = lines[:self.max_lines]

            last = lines[-1]

            while (
                self.font.size(last + "...")[0] > max_width
                and len(last) > 0
            ):
                last = last[:-1]

            lines[-1] = last + "..."

        return lines

    def draw(self, surface: pg.Surface) -> None:
        """Draw the element on the target surface.

        Args:
            surface (pg.Surface): Destination surface.
        """

        pg.draw.rect(
            surface,
            self.bg_color,
            self.rect,
            border_radius=self.border_radius
        )

        pg.draw.rect(
            surface,
            self.border_color,
            self.rect,
            width=2,
            border_radius=self.border_radius
        )

        padding = 10
        max_text_width = self.rect.width - padding * 2

        lines = self.wrap_text(max_text_width)

        line_height = self.font.get_height()
        total_height = len(lines) * line_height

        start_y = self.rect.centery - total_height // 2

        for i, line in enumerate(lines):
            text_surface = self.font.render(
                line,
                True,
                self.text_color
            )

            text_rect = text_surface.get_rect(
                centerx=self.rect.centerx,
                y=start_y + i * line_height
            )

            surface.blit(text_surface, text_rect)


class Button(PCUIElement):
    """Clickable UI button with optional icon and selection state."""

    def __init__(
            self,
            text: str,
            font: pg.Font,
            x: int = 0,
            y: int = 0,
            width: int = 0,
            height: int = 0,
            icon: pg.Surface | None = None) -> None:
        """Initialize button content, geometry, and optional icon.

        Args:
            text (str): Button label text.
            font (pg.Font): Font used to render label text.
            x (int, optional): Left position in pixels.
            y (int, optional): Top position in pixels.
            width (int, optional): Initial width in pixels.
            height (int, optional): Initial height in pixels.
            icon (pg.Surface | None, optional): Optional icon surface.
        """

        super().__init__(x=x, y=y, width=width,
                         height=height, font=font,
                         text=text)
        self.icon = icon
        self.selected = False
        self.update_layout()

    def update_layout(self) -> None:
        """Recompute wrapped text, size, and centered horizontal position."""

        self.lines = self.wrap_text(SCREEN_WIDTH // 2 - 42)
        self.line_height = self.font.get_height()
        self.total_height = len(self.lines) * self.line_height
        text_surf = self.font.render(self.text, True, self.text_color)
        self.rect.width = min(text_surf.get_width() + 42, SCREEN_WIDTH // 2)
        self.rect.height = self.total_height + 42
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2

    def draw(self, surface: pg.Surface) -> None:
        """Render button visuals and text to the target surface.

        Args:
            surface (pg.Surface): Destination surface.
        """

        if self.selected and self.icon:
            img_rect = self.icon.get_rect(
                center=(self.rect.left - 42, self.rect.centery))
            surface.blit(self.icon, img_rect)

        pg.draw.rect(
            surface,
            self.bg_color,
            self.rect,
            border_radius=self.border_radius
        )

        pg.draw.rect(
            surface,
            self.border_color,
            self.rect,
            width=2,
            border_radius=self.border_radius
        )

        start_y = self.rect.centery - self.total_height // 2

        for i, line in enumerate(self.lines):
            text_surf = self.font.render(line, True, self.text_color)
            text_rect = text_surf.get_rect(centerx=self.rect.centerx,
                                           y=start_y + i * self.line_height)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        """Check whether a point is inside the button bounds.

        Args:
            pos (tuple[int, int]): Pointer position in pixels.

        Returns:
            bool: True if the point collides with the button rect.
        """
        return self.rect.collidepoint(pos)
