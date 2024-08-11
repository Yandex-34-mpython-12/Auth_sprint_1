from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi_pagination import Page

from auth_service.src.models import Role
from auth_service.src.models.data import RoleCreate
from auth_service.src.services.role import RoleService, role_services

router = APIRouter()

@router.post('/create', status_code=HTTPStatus.OK, description='Create new Role', response_model=Role)
async def create_role(
    request: Request,
    role: RoleCreate,
    service: RoleService = Depends(role_services),
) -> Role:
    role = await service.create_role(name=role.name)
    if not role:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Role is taken')
    return role


@router.get(
    '/list',
    status_code=HTTPStatus.OK,
    description='List Roles',
    response_model=Page[Role],
)
async def get_role(
    page: int = Query(1),
    items_per_page: int = Query(10),
    service: RoleService = Depends(role_services),
) -> Page[Role]:
    result = await service.get_roles()
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Role not exist')
    skip_pages = page - 1
    return Page(
        items=result[skip_pages : skip_pages + items_per_page],
        total=len(result),
        page=page,
        size=items_per_page,
    )


@router.delete(
    '/delete',
    status_code=HTTPStatus.NO_CONTENT,
    description='Delete Roles',
)
async def delete_role(
    request: Request,
    role_id: int,
    service: RoleService = Depends(role_services),
) -> None:
    result = await service.delete_role(role_id=role_id)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Permission not exist'
        )