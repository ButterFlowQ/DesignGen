package com.example.projectname.controller;

import com.example.projectname.dtos.AddItemRequest;
import com.example.projectname.dtos.UpdateItemRequest;
import com.example.projectname.entities.InventoryItem;
import com.example.projectname.entities.User;
import com.example.projectname.enums.UserRole;
import com.example.projectname.service.InventoryService;
import com.example.projectname.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

/**
 * Controller handling CRUD operations for shopkeepers' inventory items.
 */
@RestController
@RequestMapping("/shopkeepers/{shopkeeperId}/inventory")
public class InventoryController {

    @Autowired
    private InventoryService inventoryService;

    @Autowired
    private UserService userService;

    /**
     * Retrieves the inventory items for a specific shopkeeper.
     * @param shopkeeperId the ID of the shopkeeper
     * @return a ResponseEntity containing a list of inventory items
     */
    @GetMapping
    public ResponseEntity<List<InventoryItem>> getInventory(@PathVariable UUID shopkeeperId) {
        List<InventoryItem> inventory = inventoryService.getInventoryByShopkeeper(shopkeeperId);
        return ResponseEntity.ok(inventory);
    }

    /**
     * Adds a new item to the specified shopkeeper's inventory.
     * @param shopkeeperId the ID of the shopkeeper
     * @param addItemRequest the details of the item to be added
     * @return a ResponseEntity containing the added inventory item
     */
    @PostMapping
    public ResponseEntity<InventoryItem> addInventoryItem(@PathVariable UUID shopkeeperId, @RequestBody AddItemRequest addItemRequest) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

        // 2) Extract your custom principal
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("No authenticated user found.");
        }

        // If you stored your user ID in a CustomUserDetails object:
        User currentUser = userService.findByUserName(((UserDetails)authentication.getPrincipal()).getUsername());
        UUID shopkeeperId1 = currentUser.getId();
        if (!currentUser.getRole().equals(UserRole.SHOPKEEPER)) {
            throw new RuntimeException("User is not a shopkeeper");
        }
        if (!shopkeeperId.equals(shopkeeperId1)) {
            throw new RuntimeException("Shopkeeper can only update their own shops");
        }
        InventoryItem item = inventoryService.addItem(shopkeeperId, addItemRequest.getName(), addItemRequest.getPrice(), addItemRequest.getImageUrl());
        return ResponseEntity.status(201).body(item);
    }

    /**
     * Updates details of a specific inventory item for the shopkeeper.
     * @param shopkeeperId the ID of the shopkeeper
     * @param itemId the ID of the inventory item
     * @param updateItemRequest the updated details of the inventory item
     * @return a ResponseEntity containing the updated inventory item
     */
    @PutMapping("/{itemId}")
    public ResponseEntity<InventoryItem> updateInventoryItem(@PathVariable UUID shopkeeperId, @PathVariable UUID itemId, @RequestBody UpdateItemRequest updateItemRequest) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

        // 2) Extract your custom principal
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("No authenticated user found.");
        }

        // If you stored your user ID in a CustomUserDetails object:
        User currentUser = userService.findByUserName(((UserDetails)authentication.getPrincipal()).getUsername());
        UUID shopkeeperId1 = currentUser.getId();
        if (!currentUser.getRole().equals(UserRole.SHOPKEEPER)) {
            throw new RuntimeException("User is not a shopkeeper");
        }
        if (!shopkeeperId.equals(shopkeeperId1)) {
            throw new RuntimeException("Shopkeeper can only update their own shops");
        }
        InventoryItem item = inventoryService.updateItem(shopkeeperId, itemId, updateItemRequest.getName(), updateItemRequest.getPrice(), updateItemRequest.getImageUrl());
        return ResponseEntity.ok(item);
    }

    /**
     * Removes an item from the shopkeeper's inventory.
     * @param shopkeeperId the ID of the shopkeeper
     * @param itemId the ID of the inventory item
     * @return a ResponseEntity with no content
     */
    @DeleteMapping("/{itemId}")
    public ResponseEntity<?> deleteInventoryItem(@PathVariable UUID shopkeeperId, @PathVariable UUID itemId) {
        inventoryService.removeItem(shopkeeperId, itemId);
        return ResponseEntity.noContent().build();
    }
}