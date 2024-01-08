ViewImagesComponent = {
    props: ['value'],
    template: `
        <div style="text-align: center;">
            <img v-for="image in value" style="width: 100px; margin-left: 15px;" :src="image.image" :key="image.pk">
        </div>
        <slot/>
    `,
}
