import pytest

from qcm_generator.main_cli import transform_image_includes


@pytest.mark.parametrize(
    ('input_content', 'expected_output'),
    [
        (
            r'\includegraphics[width=0.5\textwidth]{path/to/image.png}',
            r'\includegraphics[width=0.5\textwidth]{../../path/to/image.png}',
        ),
        (
            r'\includegraphics{another/path/to/image.jpg}',
            r'\includegraphics{../../another/path/to/image.jpg}',
        ),
        (
            r'\includegraphics[width=0.3\textwidth]{/absolute/path/to/image.png}',
            r'\includegraphics[width=0.3\textwidth]{/absolute/path/to/image.png}',
        ),
        (
            r'\includegraphics[width=0.5\textwidth]{C:/absolute/path/to/image.png}',
            r'\includegraphics[width=0.5\textwidth]{C:/absolute/path/to/image.png}',
        ),
        (
            r'\includegraphics[width=0.5\textwidth]{D:\\absolute\\path\\to\\image.jpg}',
            r'\includegraphics[width=0.5\textwidth]{D:\\absolute\\path\\to\\image.jpg}',
        ),
        (
            r"""
        \includegraphics[height=5cm]{relative/path/to/image1.jpg}
        \includegraphics{relative/path/to/image2.png}
        """,
            r"""
        \includegraphics[height=5cm]{../../relative/path/to/image1.jpg}
        \includegraphics{../../relative/path/to/image2.png}
        """,
        ),
        (
            r'No graphics included here.',
            r'No graphics included here.',
        ),
    ],
)
def test_transform_image_includes(input_content: str, expected_output: str) -> None:
    assert transform_image_includes(input_content.strip()) == expected_output.strip()
