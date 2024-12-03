from pathlib import Path
from shiny import App, ui, render

here = Path(__file__).parent

app_ui = ui.page_fluid(
    ui.input_select("area_measure", "Area Measure:", ["zcta", "tract"]),
    ui.input_select("wealth_measure", "Wealth Measure:", ["income", "value"]),
    ui.output_image("map_image")
)

def server(input, output, session):
    @output
    @render.image
    def map_image():
        area_measure = input.area_measure()
        wealth_measure = input.wealth_measure()
        image_path = here / f"{area_measure}_{wealth_measure}.png"
        
        return {"src": image_path, "alt": f"Map showing {wealth_measure} for {area_measure}", "width": "80%"}

app = App(app_ui, server)
