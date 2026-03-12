from typing import Type, Generic, List, TypeVar
from django.db import models
from ninja_extra import route
from ninja.pagination import paginate

ModelType = TypeVar("ModelType", bound=models.Model)
SchemaType = TypeVar("SchemaType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class AsyncCRUDController(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):

    model: Type[ModelType]
    schema: Type[SchemaType]

    def get_queryset(self):
        return self.model.objects.all()

    @route.get("/", response=List[SchemaType])
    @paginate
    async def list(self):
        qs = self.get_queryset()
        return [self.schema.from_orm(obj) async for obj in qs]

    @route.get("/{obj_id}", response=SchemaType)
    async def retrieve(self, obj_id: int):
        obj = await self.get_queryset().aget(id=obj_id)
        return self.schema.from_orm(obj)

    @route.post("/", response=SchemaType)
    async def create(self, payload: CreateSchemaType):
        obj = await self.model.objects.acreate(**payload.model_dump())
        return self.schema.from_orm(obj)

    @route.patch("/{obj_id}", response=SchemaType)
    async def update(self, obj_id: int, payload: UpdateSchemaType):
        obj = await self.get_queryset().aget(id=obj_id)
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await obj.asave()
        return self.schema.from_orm(obj)

    # @route.delete("/{obj_id}")
    # async def delete(self, obj_id: int):
    #     # obj = await self.get_queryset().aget(id=obj_id)
    #     # await obj.adelete()
    #     return {"success": True}