# api.py
from flask import Flask, jsonify, request
from flask_cors import CORS # Used for handling Cross-Origin Resource Sharing
from app.sweet import Sweet
from app.sweetshop import SweetShop

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, allowing requests from different origins

shop = SweetShop() # Create an instance of your SweetShop

# --- Optional: Pre-populate some data for easy testing ---
# This block runs once when the server starts.
# It's helpful for development so you don't have to add sweets manually every time.
try:
    shop.add_sweet(Sweet(1001, "Kaju Katli", "Nut-Based", 50.0, 20))
    shop.add_sweet(Sweet(1002, "Gulab Jamun", "Milk-Based", 40.0, 15))
    shop.add_sweet(Sweet(1003, "Rasgulla", "Milk-Based", 25.0, 30))
    print("Pre-populated some sweets for testing.")
except ValueError as e:
    # This will print if you restart the server multiple times and try to add duplicates
    print(f"Warning during pre-population: {e}")


@app.route('/')
def home():
    """
    A simple home route to confirm the API is running.
    Access this in your browser at http://127.0.0.1:5000/
    """
    return "Welcome to the Sweet Shop API! Access /sweets for operations."


@app.route('/sweets', methods=['GET'])
def get_sweets():
    """
    Endpoint to retrieve all sweets currently available in the shop.
    Returns a JSON list of sweet dictionaries.
    Access this in your browser at http://127.0.0.1:5000/sweets
    """
    # Use the to_dict() method on Sweet objects for cleaner and controlled serialization
    return jsonify([s.to_dict() for s in shop.view_sweets()])


@app.route('/sweets', methods=['POST'])
def add_sweet():
    """
    Endpoint to add a new sweet to the shop.
    Expects JSON data in the request body:
    {"sweet_id": int, "name": str, "category": str, "price": float, "quantity": int}
    """
    data = request.get_json() # Use get_json() to parse incoming JSON data

    if not data:
        return jsonify({'error': 'Invalid JSON data provided or missing'}), 400

    try:
        # Extract data using the expected keys, e.g., 'sweet_id'
        sweet_id = data['sweet_id']
        name = data['name']
        category = data['category']
        price = data['price']
        quantity = data['quantity']

        # Create a Sweet object and add it to the shop
        new_sweet = Sweet(sweet_id, name, category, price, quantity)
        shop.add_sweet(new_sweet)
        
        # Return success message and the created sweet data with 201 Created status
        return jsonify({'message': 'Sweet added successfully', 'sweet': new_sweet.to_dict()}), 201

    except KeyError as e:
        # Handle cases where required fields are missing from the JSON payload
        return jsonify({'error': f"Missing required field: '{e}'. "
                                 "Required fields are sweet_id, name, category, price, quantity."}), 400
    except ValueError as e:
        # Handle validation errors from Sweet constructor or duplicate ID from add_sweet method
        error_message = str(e)
        if "already exists" in error_message:
            # Return 409 Conflict if a sweet with the same ID already exists
            return jsonify({'error': error_message}), 409
        else:
            # Return 400 Bad Request for other validation errors (e.g., negative price/quantity)
            return jsonify({'error': error_message}), 400
    except Exception as e:
        # Catch any other unexpected errors that might occur
        return jsonify({'error': f"An unexpected server error occurred: {str(e)}"}), 500


@app.route('/sweets/<int:sweet_id>', methods=['DELETE'])
def delete_sweet(sweet_id):
    """
    Endpoint to delete a sweet by its ID.
    The sweet_id is passed as part of the URL path.
    """
    try:
        shop.delete_sweet(sweet_id)
        # Return 200 OK for successful deletion
        return jsonify({'message': f'Sweet with ID {sweet_id} deleted successfully'}), 200
    except ValueError as e:
        # Handle if the sweet with the given ID is not found
        return jsonify({'error': str(e)}), 404 # 404 Not Found if sweet_id doesn't exist
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({'error': f"An unexpected server error occurred: {str(e)}"}), 500


# --- New Endpoint: Search Sweets (Example) ---
@app.route('/sweets/search', methods=['GET'])
def search_sweets_api():
    """
    Endpoint to search for sweets based on query parameters.
    Example usage:
    - http://127.0.0.1:5000/sweets/search?name=kaju
    - http://127.0.0.1:5000/sweets/search?category=Milk-Based
    - http://127.0.0.1:5000/sweets/search?price_min=10&price_max=60
    - http://127.0.0.1:5000/sweets/search?name=gulab&category=Milk-Based
    """
    # Get query parameters from the URL
    name = request.args.get('name')
    category = request.args.get('category')
    # Use type=float to automatically convert price parameters
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)

    try:
        # Call the search_sweets method from your SweetShop
        results = shop.search_sweets(
            name=name,
            category=category,
            price_min=price_min,
            price_max=price_max
        )
        # Return the search results as a JSON list of sweet dictionaries
        return jsonify([s.to_dict() for s in results]), 200
    except Exception as e:
        # Catch any errors during the search operation
        return jsonify({"error": f"Error during search: {str(e)}"}), 500


# --- You will need to add similar endpoints for: ---
# Purchase sweets endpoint
@app.route('/sweets/<int:sweet_id>/purchase', methods=['POST'])
def purchase_sweet_api(sweet_id):
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Missing quantity'}), 400
    try:
        shop.purchase_sweet(sweet_id, int(data['quantity']))
        return jsonify({'message': f'Purchased {data["quantity"]} of sweet ID {sweet_id}'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# Restock sweets endpoint
@app.route('/sweets/<int:sweet_id>/restock', methods=['POST'])
def restock_sweet_api(sweet_id):
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Missing quantity'}), 400
    try:
        shop.restock_sweet(sweet_id, int(data['quantity']))
        return jsonify({'message': f'Restocked {data["quantity"]} of sweet ID {sweet_id}'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
# 1. Update Sweet Details (PUT or PATCH /sweets/<int:sweet_id>)
#    - Expects JSON body with fields to update (name, category, price, quantity)
# 2. Purchase Sweets (POST /sweets/<int:sweet_id>/purchase)
#    - Expects JSON body: {"quantity": int}
# 3. Restock Sweets (POST /sweets/<int:sweet_id>/restock)
#    - Expects JSON body: {"quantity": int}
# 4. Sort Sweets (GET /sweets/sort?key=name&reverse=true)
#    - Returns sorted list of sweets

if __name__ == '__main__':
    # Run the Flask app in debug mode. This enables auto-reloading and a debugger.
    app.run(debug=True)