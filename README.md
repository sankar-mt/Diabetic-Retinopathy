This project applies deep learning to detect Diabetic Retinopathy (DR) from retinal fundus images using transfer learning with ResNet50. The model leverages pretrained ImageNet weights to extract high-level visual features from eye images, followed by custom classification layers that categorize the severity of DR across five stages: from No DR to Proliferative DR.

The pipeline includes all key stages of a practical medical imaging workflow:

Preprocessing: Image resizing, normalization, and label encoding for clean input to the network.

Model Training: Fine-tuning the ResNet50 backbone with dropout regularization, Adam optimizer, and categorical cross-entropy loss.

Evaluation: Tracks accuracy, loss curves, and class-wise performance to assess diagnostic reliability.

This project demonstrates how transfer learning can significantly improve diagnostic accuracy in medical imaging tasks with limited datasets; offering an efficient baseline for future experimentation with attention-based or ensemble architectures.
