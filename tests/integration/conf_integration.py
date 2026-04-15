async def _register(client, email: str, password: str = "StrongPass1!"):
    return await client.post("/auth/register", json={"email": email, "password": password})


async def _login(client, email: str, password: str = "StrongPass1!"):
    return await client.post("/auth/login", json={"email": email, "password": password})


def _auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}