package com.example.projectname.dtos;

import java.util.List;
import java.util.UUID;

/**
 * DTO for placing a new order.
 */
public class PlaceOrderRequest {

    private UUID shopkeeperId;
    private List<OrderItemRequest> items;

    /**
     * Gets the shopkeeper ID.
     *
     * @return the shopkeeper ID
     */
    public UUID getShopkeeperId() {
        return shopkeeperId;
    }

    /**
     * Sets the shopkeeper ID.
     *
     * @param shopkeeperId the shopkeeper ID to set
     */
    public void setShopkeeperId(UUID shopkeeperId) {
        this.shopkeeperId = shopkeeperId;
    }

    /**
     * Gets the list of order items.
     *
     * @return the list of order items
     */
    public List<OrderItemRequest> getItems() {
        return items;
    }

    /**
     * Sets the list of order items.
     *
     * @param items the list of order items to set
     */
    public void setItems(List<OrderItemRequest> items) {
        this.items = items;
    }
}