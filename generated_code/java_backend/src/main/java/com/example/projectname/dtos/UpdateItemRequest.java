package com.example.projectname.dtos;

import java.math.BigDecimal;

/**
 * DTO for updating an existing inventory item.
 */
public class UpdateItemRequest {

    private String name;
    private BigDecimal price;
    private String imageUrl;

    public UpdateItemRequest() {
    }

    public UpdateItemRequest(String name, BigDecimal price, String imageUrl) {
        this.name = name;
        this.price = price;
        this.imageUrl = imageUrl;
    }

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
     * @param name the new name of the item
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
     * @param price the new price of the item
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
     * @param imageUrl the new image URL of the item
     */
    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}