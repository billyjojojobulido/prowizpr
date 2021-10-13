from django.shortcuts import render

@require_http_methods(["POST"])
def show(request):
    response = {}
    try:
        query = json.loads(request.body.decode()).get("user")

        if query is None:
            query = ""
        response = {'status': 'success', 'query': query, 'msg': 'query valid'}
        # allows the query to proceed
        return JsonResponse(response)
        # TODO: authorisation
    except Exception as e:
        response['status'] = 'success'
        response['query'] = ''
        response['error_info'] = 'query transmit error'
        print(e)
        return JsonResponse(response)