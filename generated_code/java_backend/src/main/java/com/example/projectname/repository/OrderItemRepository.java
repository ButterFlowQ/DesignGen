package com.example.projectname.repository;

import com.example.projectname.entities.OrderItem;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

/**
 * Repository interface for performing CRUD operations on OrderItem entities.
 */
public interface OrderItemRepository extends JpaRepository<OrderItem, UUID> {
    // Additional query methods can be defined here if needed
}
