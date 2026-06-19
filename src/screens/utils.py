import pygame as pg
from constants import SCREEN_WIDTH


class PCUIElement:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        bg_color: str = "black",
        text_color: str = "yellow",
        border_color: str = "yellow",
        border_radius: int = 12,
        font: pg.Font | None = None,
        max_lines: int = 2
    ) -> None:
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.max_lines = max_lines
        self.font = font or pg.font.SysFont(None, 30)

    def wrap_text(self, max_width: int) -> list[str]:
        """Return a list of lines wrapped to max_width."""
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
    def __init__(
            self,
            y: int,
            text: str,
            x: int = 0,
            width: int = 0,
            height: int = 0,
            icon: pg.Surface | None = None) -> None:
        super().__init__(x, y, width, height, text)
        self.icon = icon
        self.hovered = False
        self.selected = False
        self.update_layout()

    def update_layout(self) -> None:
        self.lines = self.wrap_text(SCREEN_WIDTH // 2 - 42)
        self.line_height = self.font.get_height()
        self.total_height = len(self.lines) * self.line_height

        text_surf = self.font.render(self.text, True, self.text_color)
        
        self.rect.width = min(text_surf.get_width() + 42, SCREEN_WIDTH // 2)
        self.rect.height = self.total_height + 42
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2


    def draw(self, surface: pg.Surface) -> None:
        if self.selected or self.hovered:
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
        return self.rect.collidepoint(pos)

    def update(self, pos: tuple[int, int]) -> None:
        self.hovered = self.rect.collidepoint(pos)
