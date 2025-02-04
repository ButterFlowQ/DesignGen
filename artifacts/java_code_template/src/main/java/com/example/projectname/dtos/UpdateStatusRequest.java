package com.example.projectname.dtos;

import com.example.projectname.enums.OrderStatus;

/**
 * DTO for updating the status of an order.
 */
public class UpdateStatusRequest {

    private OrderStatus status;

    /**
     * Gets the status of the order.
     *
     * @return the current status of the order
     */
    public OrderStatus getStatus() {
        return status;
    }

    /**
     * Sets the status of the order.
     *
     * @param status the new status to set for the order
     */
    public void setStatus(OrderStatus status) {
        this.status = status;
    }
}