package com.example.projectname.dtos;

import java.math.BigDecimal;

/**
 * DTO for adding a new inventory item.
 */
public class AddItemRequest {
    private String name;
    private BigDecimal price;
    private String imageUrl;

    /**
     * Gets the name of the inventory item.
     *
     * @return the name of the item
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the name of the inventory item.
     *
     * @param name the name to set
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Gets the price of the inventory item.
     *
     * @return the price of the item
     */
    public BigDecimal getPrice() {
        return price;
    }

    /**
     * Sets the price of the inventory item.
     *
     * @param price the price to set
     */
    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    /**
     * Gets the image URL of the inventory item.
     *
     * @return the image URL of the item
     */
    public String getImageUrl() {
        return imageUrl;
    }

    /**
     * Sets the image URL of the inventory item.
     *
     * @param imageUrl the image URL to set
     */
    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}