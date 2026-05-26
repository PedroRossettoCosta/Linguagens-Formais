export const DEFAULT_RITUAL_CODE = `Sanguis led = 13;
Sanguis_Fluens pressao = 1.0;

Vazium Exordium() {
    Revelare("Iniciando a estufa inteligente...");
    Habitus(led, Ignis);
}

Vazium Inferna() {
    pressao = pressao + 0.5;

    Si (pressao > 1.2) {
        Revelare("Cuidado! Pressao subiu muito!");
        Incantare(led, Ignis);
        Mora(1000);
        Incantare(led, Tenebrae);
    }
}`;
