// Global
float PI = 3.1415;

struct EleGosta {
    int a = 0;
    float b = 0.0;
    string c = "ueepa";
    char d = 'D';
};

float sqrt(int x) {
    return 2;
}

bool test_while(int a, int b) {
    while (a < b) {
        a++; // Incrementa
        b--; // Decrementa
    }
    return true;
}

bool test_for(int a, int b) {
    for (int i = 0; i < a; i++) {
        b += i;
    }

    for (;;) {
        a += b;
        b += a;
        
        if (a > b) {
            return true;
        }
    }

    return false;
}

long test_if(int a, int b) {
    if ((a < 0) | (b < 0)) {
        printf("argumentos invalidos");
    }

    if (a > b) {
        printf("maior");
    }
    else if (a < b) {
        printf("menor");
    }
    else {
        printf("igual");
    }
}

int main () {
    int wrong_square_of_two = (1e-35 + 1e-10) * 2 * 2 + (0.1 * 0.02);
}
