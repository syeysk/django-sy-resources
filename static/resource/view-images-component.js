ViewImagesComponent = {
    props: ['value'],
    template: `
        <div style="text-align: center;">
            <img v-for="image in value" style="width: 100px; margin-right: 15px;" :src="image.image" :key="image.pk">
        </div>
        <slot/>
    `,
}
