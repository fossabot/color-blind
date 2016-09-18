@0x854f626adf4f2f1f

struct body {
    mass @0 :Float64;
    moment @1 :Float64;
    enum type {
        dynamic @0;
        kinematic @1;
        static @2;
    }
}

