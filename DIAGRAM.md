table metals {
  id int pk
  metal varchar
  price float 
}


table sizes {
  id int pk
  carets float
  price float
}


table styles {
  id int pk
  style varchar
  price float
}


table customOrders {
  id int pk
  metalId int
  sizeId int
  styleId int
  timestamp datetime
}



Ref: "sizes"."id" < "customOrders"."sizeId"

Ref: "styles"."id" < "customOrders"."styleId"

Ref: "metals"."id" < "customOrders"."metalId"

