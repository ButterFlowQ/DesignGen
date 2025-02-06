package com.example.projectname.repository;

import com.example.projectname.entities.InventoryItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Repository interface for performing CRUD operations on InventoryItem entities.
 */
@Repository
public interface InventoryItemRepository extends JpaRepository<InventoryItem, UUID> {

    /**
     * Finds all inventory items associated with a specific shopkeeper.
     *
     * @param shopkeeperId the UUID of the shopkeeper
     * @return a list of inventory items
     */
    List<InventoryItem> findByShopkeeperId(UUID shopkeeperId);

    Optional<InventoryItem> findByIdAndShopkeeperId(UUID itemId, UUID shopkeeperId);
}