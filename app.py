from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'true').lower() == 'true'
    )
@app.errorhandler(500)
def handle_500_error(e):
    return {"message": str(e), "success": False}, 500