import asyncio
import pyvts

plugin_info = {
    'plugin_name': 'wAIfu',
    'developer': 'Noop corp',
    'authentication_token_path': './token.txt'
}
async def main():
    # Create a new VTube Studio API Client
    myvts = pyvts.vts(plugin_info=plugin_info)

    # Connect to the VTube Studio Server
    await myvts.connect()

    # Request and use token for authentication
    await myvts.request_authenticate_token()
    print("token add")
    await myvts.request_authenticate()
    print("token save")

    # Add a new parameter
    new_parameter_name = "start_parameter"
    await myvts.request(myvts.vts_request.requestCustomParameter(new_parameter_name))

# Run the main coroutine
asyncio.run(main())

