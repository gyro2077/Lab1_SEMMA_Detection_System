// Malas prácticas: uso de any, nombres poco claros, mezcla de responsabilidades
function process(d: any) {
    if (d.items && d.items.length > 0) {
        let t = 0;
        for (let i = 0; i < d.items.length; i++) {
            t += d.items[i].p; // ¿Qué es 'p'?
        }

        // Calcula impuesto (número mágico 0.12)
        t = t + (t * 0.12);

        // Valida inventario, guarda en DB y envía email todo junto...
        console.log("Guardando en base de datos...");
        console.log(`Enviando correo a ${d.email}`);

        return t;
    }
    return -1;
}