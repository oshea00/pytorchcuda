from langchain_core.runnables.graph import CurveStyle, NodeColors, MermaidDrawMethod

def draw_graph(graph, output_file_path):
    graph.draw_mermaid_png(
        curve_style=CurveStyle.LINEAR,
        node_colors=NodeColors(start="#ffdfba", end="#baffc9", other="#fad7de"),
        wrap_label_n_words=9,
        output_file_path=output_file_path,
        draw_method=MermaidDrawMethod.PYPPETEER,
        background_color="white",
        padding=10
    )

def draw_ascii_graph(graph):
    graph.print_ascii()

