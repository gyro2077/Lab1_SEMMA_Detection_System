// 1. Definimos Interfaces (Contratos de datos claros)
interface Product {
    id: string;
    name: string;
    price: number;
}

interface User {
    id: string;
    email: string;
    name: string;
}

interface Order {
    user: User;
    products: Product[];
}

// 2. Eliminamos "Números Mágicos" usando constantes
const TAX_RATE = 0.12;

// 3. Clases de servicio con Responsabilidad Única
class TaxCalculator {
    static calculate(amount: number): number {
        return amount * TAX_RATE;
    }
}

class EmailService {
    sendOrderConfirmation(email: string, total: number): void {
        // Lógica real de envío de correo
        console.log(`📧 Enviando confirmación a ${email}. Total: $${total.toFixed(2)}`);
    }
}

class OrderRepository {
    save(order: Order): void {
        // Lógica de base de datos
        console.log(`💾 Guardando orden de ${order.user.name} en la base de datos.`);
    }
}

// 4. Clase principal orquestadora (Lógica de negocio limpia)
class OrderProcessor {
    constructor(
        private readonly emailService: EmailService,
        private readonly orderRepository: OrderRepository
    ) { }

    public processOrder(order: Order): number {
        this.validateOrder(order);

        const subtotal = this.calculateSubtotal(order.products);
        const tax = TaxCalculator.calculate(subtotal);
        const total = subtotal + tax;

        this.orderRepository.save(order);
        this.emailService.sendOrderConfirmation(order.user.email, total);

        return total;
    }

    // Métodos privados pequeños y descriptivos
    private validateOrder(order: Order): void {
        if (!order.products || order.products.length === 0) {
            throw new Error("La orden debe contener al menos un producto.");
        }
    }

    private calculateSubtotal(products: Product[]): number {
        return products.reduce((sum, product) => sum + product.price, 0);
    }
}

// --- Uso del código ---

const myUser: User = { id: "1", name: "Alex", email: "alex@example.com" };
const myProducts: Product[] = [
    { id: "100", name: "Teclado Mecánico", price: 150 },
    { id: "101", name: "Mouse", price: 50 }
];

const processor = new OrderProcessor(new EmailService(), new OrderRepository());

try {
    const total = processor.processOrder({ user: myUser, products: myProducts });
    console.log(`✅ Proceso finalizado. Total a pagar: $${total}`);
} catch (error) {
    console.error("Error al procesar la orden:", error);
}