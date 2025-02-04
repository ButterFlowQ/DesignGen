package com.example.projectname.dtos;

import java.util.UUID;

/**
 * DTO for specifying items in an order.
 */
public class OrderItemRequest {

    private UUID itemId;
    private Integer quantity;

    /**
     * Gets the ID of the inventory item.
     *
     * @return the item ID
     */
    public UUID getItemId() {
        return itemId;
    }

    /**
     * Sets the ID of the inventory item.
     *
     * @param itemId the item ID to set
     */
    public void setItemId(UUID itemId) {
        this.itemId = itemId;
    }

    /**
     * Gets the quantity of the item to order.
     *
     * @return the quantity
     */
    public Integer getQuantity() {
        return quantity;
    }

    /**
     * Sets the quantity of the item to order.
     *
     * @param quantity the quantity to set
     */
    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }
}