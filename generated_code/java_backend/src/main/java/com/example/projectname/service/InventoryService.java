package com.example.projectname.service;

import com.example.projectname.entities.InventoryItem;
import com.example.projectname.entities.User;
import com.example.projectname.repository.InventoryItemRepository;
import com.example.projectname.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.sql.Timestamp;
import java.util.List;
import java.util.UUID;

/**
 * Service managing business logic related to inventory items, including adding, updating, and removing items.
 */
@Service
public class InventoryService {

    @Autowired
    private InventoryItemRepository inventoryItemRepository;

    @Autowired
    private UserRepository userRepository;

    /**
     * Adds a new item to the inventory for a specific shopkeeper.
     *
     * @param shopkeeperId the ID of the shopkeeper
     * @param name the name of the inventory item
     * @param price the price of the inventory item
     * @param imageUrl the image URL of the inventory item
     * @return the added InventoryItem
     */
    public InventoryItem addItem(UUID shopkeeperId, String name, BigDecimal price, String imageUrl) {
        InventoryItem item = new InventoryItem();
        User shopkeeper = userRepository.findById(shopkeeperId)
                .orElseThrow(() -> new RuntimeException("Shopkeeper not found"));

        item.setShopkeeper(shopkeeper);
        item.setName(name);
        item.setPrice(price);
        item.setImageUrl(imageUrl);
        long now = System.currentTimeMillis();
        item.setCreatedAt(new Timestamp(now));
        return inventoryItemRepository.save(item);
    }

    /**
     * Updates an existing inventory item for a specific shopkeeper.
     *
     * @param shopkeeperId the ID of the shopkeeper
     * @param itemId the ID of the inventory item
     * @param name the updated name of the inventory item
     * @param price the updated price of the inventory item
     * @param imageUrl the updated image URL of the inventory item
     * @return the updated InventoryItem
     */
    public InventoryItem updateItem(UUID shopkeeperId, UUID itemId, String name, BigDecimal price, String imageUrl) {
        InventoryItem item = inventoryItemRepository.findByIdAndShopkeeperId(itemId, shopkeeperId)
                .orElseThrow(() -> new IllegalArgumentException("Item not found"));
        item.setName(name);
        item.setPrice(price);
        item.setImageUrl(imageUrl);
        return inventoryItemRepository.save(item);
    }

    /**
     * Removes an item from the inventory for a specific shopkeeper.
     *
     * @param shopkeeperId the ID of the shopkeeper
     * @param itemId the ID of the inventory item
     */
    public void removeItem(UUID shopkeeperId, UUID itemId) {
        InventoryItem item = inventoryItemRepository.findByIdAndShopkeeperId(itemId, shopkeeperId)
                .orElseThrow(() -> new IllegalArgumentException("Item not found"));
        inventoryItemRepository.delete(item);
    }

    /**
     * Retrieves the inventory items for a specific shopkeeper.
     *
     * @param shopkeeperId the ID of the shopkeeper
     * @return a list of InventoryItem
     */
    public List<InventoryItem> getInventoryByShopkeeper(UUID shopkeeperId) {
        return inventoryItemRepository.findByShopkeeperId(shopkeeperId);
    }
}