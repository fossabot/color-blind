@0xb4a7b99a453b3ec7 

struct shape {
    elasticity @0 :Float64;
    friction @1 :Float64;
    radius @2 :Float64;
    union {
        circle :group {
            offset @4 :List(Float64);
        }
        polyon :group {
            vertices @5 :List(List(Float64));
        }
        segment :group {
            start @6 :List(List(Float64));
            end @7 :List(List(Float64));
        }
    }
}
