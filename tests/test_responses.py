from utils.responses import DatabaseErrorResponse, NotFoundErrorResponse, TimeoutErrorResponse


class TestSpecificErrorResponses:
    def test_not_found_error_response(self):
        response = NotFoundErrorResponse()
        assert response.status_code == 404
        assert response.body.decode() == '{"detail":"Not Found"}'

    def test_timeout_error_response(self):
        response = TimeoutErrorResponse()
        assert response.status_code == 408
        assert response.body.decode() == '{"detail":"Process timed out"}'

    def test_database_error_response(self):
        response = DatabaseErrorResponse()
        assert response.status_code == 500
        assert (
            response.body.decode()
            == '{"detail":"Could not connect or perform the operation to the database"}'
        )

        # Test with debug_message
        debug_msg = "Sample Debug Message"
        response = DatabaseErrorResponse(debug_message=debug_msg)
        expected_body = (
            '{"detail":"' + DatabaseErrorResponse.detail + '","debug_message":"' + debug_msg + '"}'
        )
        assert response.body.decode() == expected_body
