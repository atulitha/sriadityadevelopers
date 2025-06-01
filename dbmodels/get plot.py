from typing import List, Dict

from flask import Flask, current_app

from dbmodels.create import Project, db


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


def get_plots_by_project_id(project_id: int) -> List[Dict]:
    """
    Retrieve plots information for a given project ID.

    Args:
        project_id: The ID of the project to query

    Returns:
        List of dictionaries containing plot information
    """
    try:
        with create_app().app_context():
            project = Project.query.get_or_404(project_id)
            return [{
                'plot_id': plot.id,
                'plot_number': plot.plot_number,
                'size': plot.size,
                'price': plot.price,
                'status': plot.status,
                'project_name': project.name,
                'project_location': project.location
            } for plot in project.plots]
    except Exception as e:
        current_app.logger.error(f"Error retrieving plots for project {project_id}: {str(e)}")
        return []

print(get_plots_by_project_id(1))