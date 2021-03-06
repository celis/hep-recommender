from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from hep_recommender_app.recommender.forms import InputForm
from hep_recommender_app.inspirehep_api_wrapper.service.inspire_api import InspireAPI
from hep_recommender_app.configuration import Configuration
from hep_recommender_app.utils import load_model
from hep_recommender_app.recommender.model import RecommenderModel

app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
bootstrap = Bootstrap()
bootstrap.init_app(app)

config = Configuration()
gensim_wrapper = load_model(config)
model = RecommenderModel(gensim_wrapper)
inspire_api = InspireAPI()


@app.route("/", methods=["GET"])
def index():
    article = None
    recommendations = None
    form = InputForm(request.args)

    if form.validate():
        article = request.args.get("article")

        article = inspire_api.data(article)

        recommendations = model.predict(article)

        if recommendations:
            recommendations = [
                inspire_api.data(recommendation) for recommendation in recommendations
            ]

    return render_template(
        "index.html", form=form, article=article, recommendations=recommendations
    )


if __name__ == "__main__":

    app.run(threaded=True, port=5000, debug=True)
