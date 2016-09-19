@0x854f626adf4f2f1f;

struct Body {
    mass @0 :Float64;
    moment @1 :Float64;
    type @2 :Type;
    enum Type {
        dynamic @0;
        kinematic @1;
        static @2;
    }
}

