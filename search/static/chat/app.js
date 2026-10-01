console.log("🔥🔥🔥 NEW CHAT JAVASCRIPT LOADED 🔥🔥🔥");

document.addEventListener("DOMContentLoaded", function () {
    console.log("CHAT DOM READY");

    // =====================================================
    // ELEMENTS
    // =====================================================
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message-input");
    const chatBox = document.getElementById("chat-box");
    const clearHistoryButton = document.getElementById("clear-history");
    const sendButton = document.getElementById("send-button");

    // =====================================================
    // CSRF
    // =====================================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // =====================================================
    // SCROLL
    // =====================================================
    function scrollToBottom() {
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // =====================================================
    // USER MESSAGE
    // =====================================================
    function addUserMessage(message) {
        const element = document.createElement("div");
        element.className = "message user-message";

        const bubble = document.createElement("div");
        bubble.className = "bubble user-bubble";

        const name = document.createElement("div");
        name.className = "name";
        name.textContent = "You";

        const text = document.createElement("p");
        text.textContent = message;

        bubble.appendChild(name);
        bubble.appendChild(text);
        element.appendChild(bubble);
        chatBox.appendChild(element);

        scrollToBottom();
    }

    // =====================================================
    // TYPING
    // =====================================================
    function addTypingIndicator() {
        if (document.getElementById("typing")) {
            return;
        }

        const typing = document.createElement("div");
        typing.id = "typing";
        typing.className = "message assistant-message";

        typing.innerHTML = `
            <div class="avatar">
                AI
            </div>
            <div class="bubble assistant-bubble">
                <div class="name">
                    Assistant
                </div>
                <div class="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        chatBox.appendChild(typing);
        scrollToBottom();
    }

    // =====================================================
    // REMOVE TYPING
    // =====================================================
    function removeTypingIndicator() {
        const typing = document.getElementById("typing");
        if (typing) {
            typing.remove();
        }
    }

    // =====================================================
    // VIEW PRODUCT BUTTON
    // =====================================================
    function createViewProductButton(product) {
        if (!product || !product.url) {
            console.warn("Missing product URL:", product);
            return null;
        }

        const button = document.createElement("a");
        button.href = product.url;
        button.textContent = "View Product";
        button.className = "product-view-button";

        button.style.display = "inline-block";
        button.style.marginTop = "14px";
        button.style.padding = "10px 16px";
        button.style.background = "#10a37f";
        button.style.color = "#ffffff";
        button.style.textDecoration = "none";
        button.style.borderRadius = "8px";
        button.style.fontWeight = "600";
        button.style.cursor = "pointer";

        return button;
    }

    // =====================================================
    // PRODUCT CARD
    // =====================================================
    function createProductCard(product, number) {
        if (!product) {
            return null;
        }

        console.log("CREATING PRODUCT CARD:", product);

        const card = document.createElement("div");
        card.className = "document-card product-card";

        card.style.marginTop = "12px";
        card.style.padding = "14px";
        card.style.border = "1px solid #ddd";
        card.style.borderRadius = "10px";
        card.style.background = "#ffffff";

        // =================================================
        // TITLE
        // =================================================
        const titleRow = document.createElement("div");
        titleRow.style.display = "flex";
        titleRow.style.alignItems = "center";
        titleRow.style.gap = "8px";

        if (number !== undefined) {
            const numberElement = document.createElement("strong");
            numberElement.textContent = number + ".";
            titleRow.appendChild(numberElement);
        }

        const title = document.createElement("strong");
        title.textContent = "🛍 " + (product.name || "Product");
        titleRow.appendChild(title);
        card.appendChild(titleRow);

        // =================================================
        // PRICE
        // =================================================
        if (product.price !== null && product.price !== undefined) {
            const price = document.createElement("div");
            price.className = "score";
            price.textContent = "Price: $" + product.price;
            card.appendChild(price);
        }

        // =================================================
        // STOCK
        // =================================================
        if (product.stock_count !== null && product.stock_count !== undefined) {
            const stock = document.createElement("div");
            stock.className = "score";
            const count = Number(product.stock_count);

            if (count > 0) {
                stock.textContent = "Stock: " + count + " available";
            } else {
                stock.textContent = "Stock: Out of stock";
            }

            card.appendChild(stock);
        }

        // =================================================
        // CATEGORY
        // =================================================
        if (product.category) {
            const category = document.createElement("div");
            category.className = "score";
            category.textContent = "Category: " + product.category;
            card.appendChild(category);
        }

        // =================================================
        // DESCRIPTION
        // =================================================
        if (product.description) {
            const description = document.createElement("div");
            description.className = "product-description";
            description.style.marginTop = "6px";
            description.style.color = "#555";
            description.style.fontSize = "14px";
            description.textContent = product.description;
            card.appendChild(description);
        }

        // =================================================
        // VIEW PRODUCT
        // =================================================
        const button = createViewProductButton(product);
        if (button) {
            card.appendChild(button);
        }

        return card;
    }

    // =====================================================
    // ADD PRODUCTS
    // =====================================================
    function addProducts(bubble, products) {
        if (!Array.isArray(products) || products.length === 0) {
            return;
        }

        console.log("ADDING PRODUCTS:", products);

        const container = document.createElement("div");
        container.className = "chat-products";

        products.forEach(function (product, index) {
            const card = createProductCard(product, index + 1);
            if (card) {
                container.appendChild(card);
            }
        });

        bubble.appendChild(container);
    }

    function addOrders(bubble, orders) {
        if (!Array.isArray(orders) || orders.length === 0) return;

        const container = document.createElement("div");
        container.className = "chat-products";

        orders.forEach(function (order) {
            const card = document.createElement("div");
            card.className = "document-card product-card";

            const title = document.createElement("strong");
            title.textContent = "Order #" + (order.id || order.order_number || "");
            card.appendChild(title);

            const status = document.createElement("div");
            status.className = "score";
            status.textContent =
                "Status: " + (order.status_display || order.order_status || "Unknown") +
                " | Payment: " + (order.payment_status || "Unknown");
            card.appendChild(status);

            const total = document.createElement("div");
            total.className = "score";
            total.textContent = "Total: $" + (order.total_price || "0.00");
            card.appendChild(total);

            if (order.estimated_delivery_date) {
                const delivery = document.createElement("div");
                delivery.className = "score";
                delivery.textContent = "Estimated delivery: " + order.estimated_delivery_date;
                card.appendChild(delivery);
            }

            if (Array.isArray(order.items) && order.items.length > 0) {
                const items = document.createElement("div");
                items.className = "score";
                items.textContent = order.items.map(function (item) {
                    return (item.product_name || "Product") + " x" + item.quantity;
                }).join(" | ");
                card.appendChild(items);
            }

            container.appendChild(card);
        });

        bubble.appendChild(container);
    }

    function addCart(bubble, cart) {
        if (!cart || !Array.isArray(cart.items)) return;

        const container = document.createElement("div");
        container.className = "chat-products";

        if (cart.items.length === 0) {
            const empty = document.createElement("div");
            empty.className = "document-card product-card";
            empty.textContent = "Your cart is empty.";
            container.appendChild(empty);
        }

        cart.items.forEach(function (item) {
            const card = document.createElement("div");
            card.className = "document-card product-card";
            card.textContent =
                (item.product_name || "Product") +
                " | Quantity: " + item.quantity +
                " | $" + (item.total_price || "0.00");
            container.appendChild(card);
        });

        const total = document.createElement("strong");
        total.textContent = "Cart total: $" + (cart.total_price || "0.00");
        container.appendChild(total);
        bubble.appendChild(container);
    }

    function addConfirmation(bubble, data) {
        if (!data.requires_confirmation) return;

        const controls = document.createElement("div");
        controls.className = "chat-confirmation-controls";

        ["Yes, cancel", "No, keep it"].forEach(function (label) {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = label;
            button.className = "product-view-button";
            button.addEventListener("click", function () {
                input.value = label.startsWith("Yes") ? "yes" : "no";
                form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
            });
            controls.appendChild(button);
        });

        bubble.appendChild(controls);
    }

    // =====================================================
    // ASSISTANT MESSAGE
    // =====================================================
    function addAssistantMessage(data) {
        console.log("=================================");
        console.log("ASSISTANT DATA:", data);
        console.log("TYPE:", data.type);
        console.log("PRODUCTS:", data.products);
        console.log("PRODUCT COUNT:", Array.isArray(data.products) ? data.products.length : 0);
        console.log("=================================");

        const element = document.createElement("div");
        element.className = "message assistant-message";

        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = "AI";

        const bubble = document.createElement("div");
        bubble.className = "bubble assistant-bubble";

        const name = document.createElement("div");
        name.className = "name";
        name.textContent = "Assistant";
        bubble.appendChild(name);

        const answer = document.createElement("p");
        answer.textContent = data.answer || data.error || "No answer returned.";
        answer.style.whiteSpace = "pre-line";
        bubble.appendChild(answer);

        if (Array.isArray(data.products) && data.products.length > 0) {
            addProducts(bubble, data.products);
        } else if (data.product) {
            addProducts(bubble, [data.product]);
        }

        addOrders(
            bubble,
            Array.isArray(data.orders) && data.orders.length > 0
                ? data.orders
                : (data.order ? [data.order] : [])
        );
        
        addCart(bubble, data.cart);

        if (Array.isArray(data.recommendations) && data.recommendations.length > 0) {
            addProducts(bubble, data.recommendations);
        }

        addConfirmation(bubble, data);

        element.appendChild(avatar);
        element.appendChild(bubble);
        chatBox.appendChild(element);

        scrollToBottom();
    }

    // =====================================================
    // HIDE WELCOME
    // =====================================================
    function hideWelcome() {
        const welcome = document.getElementById("welcome");
        if (welcome) {
            welcome.style.display = "none";
        }
    }

    // =====================================================
    // SEND MESSAGE
    // =====================================================
    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const message = input.value.trim();
            if (!message) {
                return;
            }

            hideWelcome();
            addUserMessage(message);

            input.value = "";
            input.focus();
            addTypingIndicator();

            if (sendButton) {
                sendButton.disabled = true;
            }

            const csrfToken = getCookie("csrftoken");
            if (!csrfToken) {
                removeTypingIndicator();
                addAssistantMessage({
                    error: "CSRF token missing. Please refresh the page."
                });

                if (sendButton) {
                    sendButton.disabled = false;
                }
                return;
            }

            try {
                const response = await fetch("/chat/message/", {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    body: new URLSearchParams({
                        message: message
                    })
                });

                const rawText = await response.text();
                console.log("RAW RESPONSE:", rawText);

                let data;
                try {
                    data = JSON.parse(rawText);
                } catch (error) {
                    console.error("JSON ERROR:", error);
                    removeTypingIndicator();
                    addAssistantMessage({
                        error: "Server returned invalid JSON."
                    });
                    return;
                }

                removeTypingIndicator();

                if (!response.ok) {
                    addAssistantMessage({
                        error: data.error || data.answer || "Server error."
                    });
                    return;
                }

                console.log("FINAL DATA:", data);
                addAssistantMessage(data);

            } catch (error) {
                console.error("CHAT REQUEST ERROR:", error);
                removeTypingIndicator();
                addAssistantMessage({
                    error: "Unable to connect to the chat server."
                });
            } finally {
                if (sendButton) {
                    sendButton.disabled = false;
                }
                input.focus();
            }
        });
    }

    // =====================================================
    // CLEAR HISTORY
    // =====================================================
    if (clearHistoryButton) {
        clearHistoryButton.addEventListener("click", async function () {
            const confirmed = confirm("Are you sure you want to clear your chat history?");
            if (!confirmed) {
                return;
            }

            const csrfToken = getCookie("csrftoken");
            if (!csrfToken) {
                alert("CSRF token missing.");
                return;
            }

            clearHistoryButton.disabled = true;

            try {
                const response = await fetch("/chat/clear-history/", {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    window.location.href = "/chat/";
                    return;
                }

                alert(data.error || "Unable to clear history.");

            } catch (error) {
                console.error(error);
                alert("Unable to clear history.");
            } finally {
                clearHistoryButton.disabled = false;
            }
        });
    }

    // =====================================================
    // SUGGESTIONS
    // =====================================================
    document.querySelectorAll(".suggestion-btn").forEach(function (button) {
        button.addEventListener("click", function () {
            input.value = button.textContent.trim();
            input.focus();
        });
    });

    // =====================================================
    // ENTER
    // =====================================================
    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                if (form) {
                    form.requestSubmit();
                }
            }
        });
    }

    // =====================================================
    // INITIAL SCROLL
    // =====================================================
    if (chatBox) {
        scrollToBottom();
    }
});