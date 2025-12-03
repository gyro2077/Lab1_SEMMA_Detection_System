<?php
/**
 * Ejemplo de código seguro - Acceso a base de datos con PDO
 */

class SecureUserRepository
{
    private $pdo;

    public function __construct($dsn, $username, $password)
    {
        $this->pdo = new PDO($dsn, $username, $password);
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    /**
     * Obtiene usuario por ID usando consultas preparadas
     */
    public function getUserById($userId)
    {
        $stmt = $this->pdo->prepare('SELECT * FROM users WHERE id = :id');
        $stmt->execute(['id' => $userId]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    /**
     * Busca usuarios por nombre de forma segura
     */
    public function searchUsers($searchTerm)
    {
        // Validar entrada
        if (strlen($searchTerm) > 50) {
            throw new InvalidArgumentException('Search term too long');
        }

        $stmt = $this->pdo->prepare(
            'SELECT id, username, email FROM users WHERE username LIKE :search LIMIT 10'
        );
        $stmt->execute(['search' => '%' . $searchTerm . '%']);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Crea nuevo usuario con validación
     */
    public function createUser($username, $email, $password)
    {
        // Validar entrada
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException('Invalid email');
        }

        // Hash seguro de contraseña
        $hashedPassword = password_hash($password, PASSWORD_ARGON2ID);

        $stmt = $this->pdo->prepare(
            'INSERT INTO users (username, email, password) VALUES (:username, :email, :password)'
        );

        $stmt->execute([
            'username' => $username,
            'email' => $email,
            'password' => $hashedPassword
        ]);

        return $this->pdo->lastInsertId();
    }
}
?>