from flask import request, jsonify, render_template

def book_visit():
    if request.method == 'POST':
        data = request.get_json()
        print("Received JSON data:", data)

        return jsonify({
            'status': 'success',
            'message': 'Site visit booked successfully',
        })
    return None