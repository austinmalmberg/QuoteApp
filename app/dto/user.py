
def UserDto(user):
    return dict(
        creation_dt=user.creation_dt,
        email=user.email,
        role=user.role
    )