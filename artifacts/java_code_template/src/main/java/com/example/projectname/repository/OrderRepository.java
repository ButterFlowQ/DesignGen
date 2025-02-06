package com.example.projectname.repository;

import com.example.projectname.entities.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

/**
 * Repository interface for performing CRUD operations on Order entities.
 */
@Repository
public interface OrderRepository extends JpaRepository<Order, UUID> {

    /**
     * Finds all orders placed by a specific customer.
     *
     * @param customerId the UUID of the customer
     * @return a list of orders associated with the given customer
     */
    List<Order> findByCustomerId(UUID customerId);

    /**
     * Finds all orders associated with a specific shopkeeper.
     *
     * @param shopkeeperId the UUID of the shopkeeper
     * @return a list of orders associated with the given shopkeeper
     */
    List<Order> findByShopkeeperId(UUID shopkeeperId);
}
